import json
import os
import sys

# Name of the file where tasks will be stored
TODO_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file. If it doesn't exist, return an empty list."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Save the list of tasks to the JSON file."""
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    
    # Generate a unique ID
    task_id = 1 if not tasks else tasks[-1]["id"] + 1
    
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo"
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(new_tasks) == len(tasks):
        print(f"Task with ID {task_id} not found.")
    else:
        save_tasks(new_tasks)
        print(f"Task {task_id} deleted successfully.")

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.")

def list_tasks(status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        if status and task["status"] != status:
            continue
        print(f"[{task['id']}] {task['description']} - Status: {task['status']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python task-cli.py <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task description.")
            return
        add_task(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 4:
            print("Please provide task ID and new description.")
            return
        update_task(int(sys.argv[2]), sys.argv[3])

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide a task ID.")
            return
        delete_task(int(sys.argv[2]))

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Please provide a task ID.")
            return
        mark_status(int(sys.argv[2]), "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Please provide a task ID.")
            return
        mark_status(int(sys.argv[2]), "done")

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            status = sys.argv[2]
            if status in ["todo", "in-progress", "done"]:
                list_tasks(status)
            else:
                print("Invalid status filter. Use: todo, in-progress, done")
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()