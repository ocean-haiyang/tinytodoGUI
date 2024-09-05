import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# File to store data
DATA_FILE = 'data.json'

# Colors
OCEAN_BLUE = '#003366'
TREE_GREEN = '#004d00'
RESET_COLOR = '#000000'

# Cute cat ASCII art
CAT_ART = """
  /\\_/\\
 ( o.o )
  > ^ <
"""

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"todos": [], "habits": [], "archive": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_today():
    return datetime.now().strftime("%Y-%m-%d %A")

def add_todo():
    task = simpledialog.askstring("Add To-Do", "Enter the task:")
    if task:
        data["todos"].append({"task": task, "done": False, "date_added": get_today()})
        save_data(data)
        update_display()

def mark_todo_done():
    if data["todos"]:
        task_num = simpledialog.askinteger("Mark To-Do as Done", "Enter the task number to mark as done:")
        if task_num and 0 < task_num <= len(data["todos"]):
            data["todos"][task_num - 1]["done"] = True
            save_data(data)
            update_display()
        else:
            messagebox.showerror("Error", "Invalid task number!")

def archive_completed_todos():
    now = datetime.now()
    to_archive = [todo for todo in data["todos"] if todo["done"] and 
                  (now - datetime.strptime(todo["date_added"], "%Y-%m-%d %A")).days >= 1]
    if to_archive:
        data["archive"].extend(to_archive)
        data["todos"] = [todo for todo in data["todos"] if not todo["done"]]
        save_data(data)
        update_display()

def delete_todo():
    if data["todos"]:
        task_num = simpledialog.askinteger("Delete To-Do", "Enter the task number to delete:")
        if task_num and 0 < task_num <= len(data["todos"]):
            del data["todos"][task_num - 1]
            save_data(data)
            update_display()
        else:
            messagebox.showerror("Error", "Invalid task number!")
    else:
        messagebox.showinfo("Info", "No to-dos available to delete.")

def delete_all_todos():
    confirm = messagebox.askyesno("Delete All To-Dos", "Are you sure you want to delete all to-dos?")
    if confirm:
        data["todos"] = []
        save_data(data)
        update_display()

def add_habit():
    habit = simpledialog.askstring("Add Habit", "Enter the habit:")
    if habit:
        data["habits"].append({"habit": habit, "completed_days": 0})
        save_data(data)
        update_display()

def complete_habit():
    if data["habits"]:
        habit_num = simpledialog.askinteger("Complete Habit", "Enter the habit number to mark as completed:")
        if habit_num and 0 < habit_num <= len(data["habits"]):
            current_days = data['habits'][habit_num - 1]['completed_days']
            new_days = simpledialog.askinteger("Update Days Completed",
                                              f"Current Days Completed: {current_days}\nEnter the number of days completed (or leave blank to keep current):",
                                              initialvalue=current_days)
            if new_days is not None:
                data['habits'][habit_num - 1]['completed_days'] = new_days
                save_data(data)
                update_display()
        else:
            messagebox.showerror("Error", "Invalid habit number!")
    else:
        messagebox.showinfo("Info", "No habits available to complete.")

def delete_habit():
    if data["habits"]:
        habit_num = simpledialog.askinteger("Delete Habit", "Enter the habit number to delete:")
        if habit_num and 0 < habit_num <= len(data["habits"]):
            del data["habits"][habit_num - 1]
            save_data(data)
            update_display()
        else:
            messagebox.showerror("Error", "Invalid habit number!")
    else:
        messagebox.showinfo("Info", "No habits available to delete.")

def delete_all_habits():
    confirm = messagebox.askyesno("Delete All Habits", "Are you sure you want to delete all habits?")
    if confirm:
        data["habits"] = []
        save_data(data)
        update_display()

def update_display():
    # Clear the existing text in the Text widget
    text_display.config(state=tk.NORMAL)
    text_display.delete(1.0, tk.END)
    
    # Insert the title and date
    text_display.insert(tk.END, "TinyToDo\n", 'title')
    text_display.insert(tk.END, f"{get_today()}\n\n", 'date')

    # Insert the cute cat art
    text_display.insert(tk.END, CAT_ART + '\n\n', 'cat')

    # Insert the To-Do List
    text_display.insert(tk.END, "To-Do List:\n", 'todo_header')
    if data["todos"]:
        for i, todo in enumerate(data["todos"], 1):
            status = "✓" if todo["done"] else "0"
            text_display.insert(tk.END, f"{i}. [{status}] {todo['task']}\n", 'todo_item')
    else:
        text_display.insert(tk.END, "No to-dos available.\n", 'todo_item')
    
    # Show number of archived to-dos
    archived_count = len(data.get("archive", []))
    text_display.insert(tk.END, f"\nNumber of Archived To-Dos: {archived_count}\n", 'todo_item')
    
    # Insert the Habit List
    text_display.insert(tk.END, "\nHabits:\n", 'habit_header')
    if data["habits"]:
        for i, habit in enumerate(data["habits"], 1):
            text_display.insert(tk.END, f"{i}. {habit['habit']} (Days Completed: {habit['completed_days']})\n", 'habit_item')
    else:
        text_display.insert(tk.END, "No habits available.\n", 'habit_item')
    
    # Apply tag colors
    text_display.tag_configure('title', foreground=OCEAN_BLUE, font=('Helvetica', 16, 'bold'), justify='center')
    text_display.tag_configure('date', foreground='#000000', font=('Helvetica', 12), justify='center')
    text_display.tag_configure('cat', font=('Courier', 16), justify='center')
    text_display.tag_configure('todo_header', foreground=OCEAN_BLUE, font=('Helvetica', 12, 'bold'))
    text_display.tag_configure('todo_item', foreground=OCEAN_BLUE)
    text_display.tag_configure('habit_header', foreground=TREE_GREEN, font=('Helvetica', 12, 'bold'))
    text_display.tag_configure('habit_item', foreground=TREE_GREEN)
    
    text_display.config(state=tk.DISABLED)

def main_gui():
    global data
    data = load_data()

    # Create the main window
    root = tk.Tk()
    root.title("TinyToDo")

    # Create a Text widget to display the lists
    global text_display
    text_display = tk.Text(root, wrap=tk.WORD, height=20, width=50)
    text_display.pack(pady=10)
    
    # Create a frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Add buttons
    tk.Button(button_frame, text="Add To-Do", command=add_todo, bg=OCEAN_BLUE, fg="white", relief='raised').grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Mark To-Do as Done", command=mark_todo_done, bg=OCEAN_BLUE, fg="white", relief='raised').grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Delete To-Do", command=delete_todo, bg=OCEAN_BLUE, fg="white", relief='raised').grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Delete All To-Dos", command=delete_all_todos, bg=OCEAN_BLUE, fg="white", relief='raised').grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="Add Habit", command=add_habit, bg=TREE_GREEN, fg="white", relief='raised').grid(row=1, column=0, padx=5)
    tk.Button(button_frame, text="Complete Habit", command=complete_habit, bg=TREE_GREEN, fg="white", relief='raised').grid(row=1, column=1, padx=5)
    tk.Button(button_frame, text="Delete Habit", command=delete_habit, bg=TREE_GREEN, fg="white", relief='raised').grid(row=1, column=2, padx=5)
    tk.Button(button_frame, text="Delete All Habits", command=delete_all_habits, bg=TREE_GREEN, fg="white", relief='raised').grid(row=1, column=3, padx=5)

    # Initialize display
    update_display()

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main_gui()
