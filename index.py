import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file, creating it if it doesn't exist"""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(data):
    """Save tasks to the JSON file"""
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    """Main entry point - processes command-line arguments"""
    if len(sys.argv) < 2:
        print("task-cli - Command line Task Manager\nUsage: python index.py <command> [options]")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    cli_handle_command(command, args)

def cli_handle_command(command, args):
    """Route command to appropriate handler"""
    case = {
        "help": help,
        "exit": exit,
        "add": add,
        "list": list,
        "update": update,
        "mark": mark,
        "mark-done": mark_done,
        "mark-in-progress": mark_in_progress,
        "mark-not-done": mark_not_done,
        "remove": remove,
        "delete": remove
        }
    handler = case.get(command, cli_invalid_command)
    handler(args)

def help(args):
    """Display help information"""
    print("""task-cli - Command line Task Manager""")
    print("\nUsage: python index.py <command> [options]")
    print("\nCommands:")
    print("  help                 Show this help message")
    print("  add <task>                        Add a new task")
    print("  list [filter]                     List tasks (filter: all, done, todo, not-done, in-progress)")
    print("  update <task_id> <description>   Update task description")
    print("  mark <task_id> <status>          Mark task with status")
    print("  done <task_id>                    Mark task as done")
    print("  in-progress <task_id>            Mark task as in progress")
    print("  not-done <task_id>               Mark task as not done")
    print("  remove <task_id>                 Remove a task")
    print("  delete <task_id>                 Delete a task (alias for remove)")
    print("  exit                              Exit the application")

def exit(args):
    """Exit the application"""
    sys.exit(0)


def add(args):
    """Add a new task"""
    if not args:
        print("Error: No task description provided. \nUsage: add <task>")
        return
    tasks = load_tasks()
    now = datetime.utcnow().isoformat() + "Z"
    new_task = {
        "id": max((t.get("id", 0) for t in tasks), default=0) + 1,
        "description": " ".join(args),
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def list(args):
    """List tasks, optionally filtered by status"""
    tasks = load_tasks()
    filter_status = args[0].lower() if args else "all"

    def normalize_status(s):
        if not s:
            return "todo"
        s = s.lower()
        if s in ("not-done", "not_done", "notdone", "todo"):
            return "todo"
        if s in ("in-progress", "in_progress", "inprogress"):
            return "in-progress"
        if s == "done":
            return "done"
        return s

    fs = normalize_status(filter_status) if filter_status != "all" else "all"

    filtered_tasks = []
    for t in tasks:
        stored = t.get("status", "todo")
        if fs == "all" or normalize_status(stored) == fs:
            filtered_tasks.append(t)
    if not filtered_tasks:
        print("No tasks found.")
        return

    for task in sorted(filtered_tasks, key=lambda x: x.get("id", 0)):
        tid = task.get("id")
        desc = task.get("description") or task.get("task")
        status = task.get("status", "todo")
        created = task.get("createdAt", "-")
        updated = task.get("updatedAt", "-")
        print(f"ID: {tid}, Description: {desc}, Status: {status}, createdAt: {created}, updatedAt: {updated}")


def update(args):
    """Update a task's description"""
    if len(args) < 2:
        print("Error: Insufficient arguments. \nUsage: update <task_id> <description>")
        return
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: Task ID must be an integer.")
        return

    new_desc = " ".join(args[1:])
    now = datetime.utcnow().isoformat() + "Z"
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            task["description"] = new_desc
            if "task" in task:
                task.pop("task", None)
            task["updatedAt"] = now
            save_tasks(tasks)
            print(f"Task ID {task_id} updated.")
            return
    print(f"Error: Task with ID {task_id} not found.")


def mark(args):
    """Mark a task with a specific status"""
    if len(args) < 2:
        print("Error: Insufficient arguments. \nUsage: mark <task_id> <status>")
        return
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: Task ID must be an integer.")
        return
    raw_status = args[1].lower()

    def normalize_target(s):
        if s in ("not-done", "not_done", "notdone"):
            return "todo"
        if s in ("todo",):
            return "todo"
        if s in ("in-progress", "in_progress", "inprogress"):
            return "in-progress"
        if s == "done":
            return "done"
        return s

    status = normalize_target(raw_status)

    tasks = load_tasks()
    now = datetime.utcnow().isoformat() + "Z"
    for task in tasks:
        if task.get("id") == task_id:
            old = task.get("status") if "status" in task else "unspecified"
            task["status"] = status
            task["updatedAt"] = now
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status} (was: {old})")
            return
    print(f"Error: Task with ID {task_id} not found.")

def mark_done(args):
    """Shorthand for marking task as done"""
    if not args:
        print("Usage: done <task_id>")
        return
    mark([args[0], "done"])


def mark_in_progress(args):
    """Shorthand for marking task as in-progress"""
    if not args:
        print("Usage: in-progress <task_id>")
        return
    mark([args[0], "in-progress"])


def mark_not_done(args):
    """Shorthand for marking task as not-done"""
    if not args:
        print("Usage: not-done <task_id>")
        return
    mark([args[0], "todo"])


def remove(args):
    """Remove a task by ID"""
    if not args:
        print("Error: No task ID provided. \nUsage: remove <task_id>")
        return
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: Task ID must be an integer.")
        return
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks)
            desc = removed.get("description") or removed.get("task")
            print(f"Task ID {task_id} removed: {desc}")
            return
    print(f"Error: Task with ID {task_id} not found.")


def cli_invalid_command(args):
    """Handle invalid commands"""
    print("Error: Invalid command. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
