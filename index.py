import json
import os
import sys

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
        "remove": remove
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
    print("  list [filter]                     List tasks (filter: all, done, not-done, in-progress)")
    print("  update <task_id> <description>   Update task description")
    print("  mark <task_id> <status>          Mark task with status")
    print("  done <task_id>                    Mark task as done")
    print("  in-progress <task_id>            Mark task as in progress")
    print("  not-done <task_id>               Mark task as not done")
    print("  remove <task_id>                 Remove a task")
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
    new_task = {
        "id": max((t.get("id", 0) for t in tasks), default=0) + 1,
        "task": " ".join(args),
        "status": "not-done"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: {new_task['task']}")

def list(args):
    """List tasks, optionally filtered by status"""
    tasks = load_tasks()
    filter_status = args[0].lower() if args else "all"
    valid = {"all", "done", "not-done", "in-progress"}
    if filter_status not in valid:
        print("Error: Invalid filter. Use 'all', 'done', 'not-done', or 'in-progress'.")
        return

    filtered_tasks = [t for t in tasks if filter_status == "all" or t.get("status") == filter_status]
    if not filtered_tasks:
        print("No tasks found.")
        return

    for task in sorted(filtered_tasks, key=lambda x: x.get("id", 0)):
        tid = task.get("id")
        desc = task.get("task") or task.get("description")
        status = task.get("status", "not-done")
        print(f"ID: {tid}, Task: {desc}, Status: {status}")



def update(args):
    """Update a task's description"""
    pass


def mark(args):
    """Mark a task with a specific status"""
    pass


def mark_done(args):
    """Shorthand for marking task as done"""
    pass


def mark_in_progress(args):
    """Shorthand for marking task as in-progress"""
    pass


def mark_not_done(args):
    """Shorthand for marking task as not-done"""
    pass


def remove(args):
    """Remove a task by ID"""
    pass


def cli_invalid_command(args):
    """Handle invalid commands"""
    pass


if __name__ == "__main__":
    main()
