import os
import json
import re

class Task:
    def __init__(self,name,description,priority):
        self.name=name
        self.description=description
        self.priority=priority
    def to_dict(self):
        return {
            "name":self.name,
            "description":self.description,
            "priority":self.priority
        }
    @staticmethod
    def from_dict(data):
        return Task(data["name"],data["description"],data["priority"])
def load_task():
    DATA_FILE="task.json"
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE,"r") as f:
            data=json.load(f)
            return [Task.from_dict(task) for task in data]
    except (json.JSONDecodeError,FileNotFoundError):
        print("error reading the file")
        return []
def save_task(tasks):
    # os.makedirs(os.path.dirname("task.json"),exist_ok=True)
    data_file="task.json"
    with open(data_file,"w") as f:
        json.dump([task.to_dict() for task in tasks],f,indent=4)
def display_menu():
    print("\n=== Task Manager Application ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")
def validate_priority(priority):
    return priority.lower() in ["high", "medium", "low"]

def validate_string(prompt, pattern=None):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty.")
            continue
        if pattern and not re.match(pattern, value):
            print("Invalid format. Try again.")
            continue
        return value

def validate_numeric(prompt, max_value):
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= max_value:
                return value
            else:
                print(f"Enter a number between 1 and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def add_task(tasks):
    print("\n--- Add New Task ---")
    name = validate_string("Enter task name: ")
    description = validate_string("Enter description: ")
    priority = validate_string("Enter priority (High/Medium/Low): ")
    if not validate_priority(priority):
        print("Invalid priority. Task creation failed.")
        return
    tasks.append(Task(name, description, priority.capitalize()))
    save_task(tasks)
    print(f"Task '{name}' added successfully!")
def view_task(tasks):
    if not tasks:
        print("no task found")
    for i,task in enumerate(tasks,start=1):
        print(f"{i}. {task.name} \t {task.description} \t Priority:{task.priority}")
def update_task(tasks):
    view_task(tasks)
    if not tasks: return
    index = validate_numeric("Enter task number to update: ", len(tasks)) - 1
    task = tasks[index]
    print("Leave blank to keep existing value.")
    new_name = input("New name: ").strip() or task.name
    new_desc = input("New description: ").strip() or task.description
    new_priority = input("New priority (High/Medium/Low): ").strip() or task.priority
    if not validate_priority(new_priority):
        print("Invalid priority. Update failed.")
        return
    tasks[index] = Task(new_name, new_desc, new_priority.capitalize())
    save_task(tasks)
    print(f"Task '{new_name}' updated successfully!")


def delete_task(tasks):
    view_task(tasks)
    if not tasks: return
    index = validate_numeric("Enter task number to delete: ", len(tasks)) - 1
    confirm = input(f"Are you sure you want to delete '{tasks[index].name}'? (y/n): ").lower()
    if confirm == "y":
        deleted = tasks.pop(index)
        save_task(tasks)
        print(f"Task '{deleted.name}' deleted successfully!")
    else:
        print("Deletion cancelled.")

tasks=load_task()
while True:
    display_menu()
    choice=input("Enter the choice")
    if choice=="1":
        add_task(tasks)
    elif choice == "2":
        view_task(tasks)
    elif choice == "3":
        update_task(tasks)
    elif choice == "4":
        delete_task(tasks)
    elif choice == "5":
        print("Exiting Task Manager. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
