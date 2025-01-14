import tkinter as tk
from tkinter import messagebox
import requests
import json


API_URL = "http://127.0.0.1:5000/tasks"


def load_tasks():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            tasks = response.json().get('tasks', [])
            task_listbox.delete(0, tk.END)
            for task in tasks:
                task_id = task['id']
                title = task['title']
                status = task['status']
                due_date = task['due_date']  # Fetch the due_date
                task_listbox.insert(tk.END, f"ID: {task_id} | Title: {title} | Status: {status} | Due Date: {due_date}")
        else:
            messagebox.showerror("Error", "Failed to fetch tasks.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def submit_task():
    title = title_entry.get()
    description = description_entry.get()
    status = status_var.get()
    due_date = due_date_entry.get()

    if not title or not description or not status or not due_date:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    task_data = {
        "title": title,
        "description": description,
        "status": status,
        "due_date": due_date
    }

    try:
        response = requests.post(API_URL, json=task_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Task created successfully!")
            load_tasks()  # Reload tasks after submission
            clear_form()
        else:
            messagebox.showerror("Error", f"Failed to create task. Status Code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def delete_task():
    selected_task = task_listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")
        return
    
    task_id = task_listbox.get(selected_task[0]).split('|')[0].split(':')[1].strip()  # Extract task ID

    try:
        response = requests.delete(f"{API_URL}/{task_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Task deleted successfully!")
            load_tasks()  # Reload tasks after deletion
        else:
            messagebox.showerror("Error", "Failed to delete task.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def update_task():
    selected_task = task_listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task to update.")
        return

    task_id = task_listbox.get(selected_task[0]).split('|')[0].split(':')[1].strip()  # Extract task ID
    title = title_entry.get()
    description = description_entry.get()
    status = status_var.get()
    due_date = due_date_entry.get()

    if not title or not description or not status or not due_date:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    task_data = {
        "title": title,
        "description": description,
        "status": status,
        "due_date": due_date
    }

    try:
        response = requests.put(f"{API_URL}/{task_id}", json=task_data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Task updated successfully!")
            load_tasks()  
        else:
            messagebox.showerror("Error", "Failed to update task.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def clear_form():
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    status_var.set("Not Started")


root = tk.Tk()
root.title("Task Management System")


tk.Label(root, text="Title").grid(row=0, column=0, padx=10, pady=5)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1, padx=10, pady=5)


tk.Label(root, text="Description").grid(row=1, column=0, padx=10, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=5)


tk.Label(root, text="Status").grid(row=2, column=0, padx=10, pady=5)
status_var = tk.StringVar()
status_var.set("Not Started")  
status_dropdown = tk.OptionMenu(root, status_var, "Not Started", "In Progress", "Completed")
status_dropdown.grid(row=2, column=1, padx=10, pady=5)


tk.Label(root, text="Due Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
due_date_entry = tk.Entry(root)

due_date_entry.grid(row=3, column=1, padx=10, pady=5)


submit_button = tk.Button(root, text="Submit Task", command=submit_task)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)


task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)


delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.grid(row=6, column=0, pady=10)

update_button = tk.Button(root, text="Update Task", command=update_task)
update_button.grid(row=6, column=1, pady=10)


load_tasks()


root.mainloop()
