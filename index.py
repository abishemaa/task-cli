import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    """Return a list of tasks from TASKS_FILE.

    If the file does not exist it is created and an empty list is returned.
    If the file contains invalid JSON, an empty list is returned.
    """
    if not os.path.exists(TASKS_FILE):
        # create file with empty list
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Warning: tasks.json contains invalid JSON. Starting with empty list.")
        return []
    except OSError as e:
        print(f"Error reading {TASKS_FILE}: {e}")
        return []

    # ensure we have a list of tasks
    if not isinstance(data, list):
        print(f"Warning: {TASKS_FILE} has unexpected format. Expected a list; got {type(data).__name__}.")
        return []
    return data


def save_tasks(tasks):
    """Write the task list to TASKS_FILE using an atomic replace.

    This writes to a temporary file and then replaces the original file.
    If writing fails, an error message is printed and an exception is raised.
    """
    tmp = TASKS_FILE + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(tasks, f, indent=2)
        # os.replace is atomic on most platforms
        os.replace(tmp, TASKS_FILE)
    except Exception as e:
        # try to clean up temp file if it exists
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        print(f"Error saving tasks: {e}")
        raise


def next_id(tasks):
    """Return the next available integer id for a new task."""
    if not tasks:
        return 1
    return max(t.get("id", 0) for t in tasks) + 1


def cmd_add(args):
    """Create a new task.

    Usage: add Buy milk
    """
    if not args:
        print("Usage: add <description>")
        return
    tasks = load_tasks()
    now = datetime.now().isoformat()
    task = {
        "id": next_id(tasks),
        "description": " ".join(args),
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(task)
    try:
        save_tasks(tasks)
    except Exception:
        print("Failed to save task. Check file permissions and available disk space.")
        return
    print("Task added (ID: {})".format(task["id"]))


def cmd_list(args):
    """List tasks.

    Optional filter values: all, todo, in-progress, done
    Example: list todo
    """
    tasks = load_tasks()
    if not args or args[0] == "all":
        filt = None
    else:
        filt = args[0]
    # "sorted(..., key=...)" returns a new list sorted by the value returned
    # from the `key` function for each element. Here we sort by the task's
    # `id` field. The `lambda x: x.get("id", 0)` is an anonymous function
    # that takes a task `x` and returns its id (or 0 if missing).
    for t in sorted(tasks, key=lambda x: x.get("id", 0)):
        # If a filter value was given (e.g. 'todo') and this task's status
        # does not match the filter, skip this task and continue to the next
        # iteration. `continue` moves control back to the top of the loop.
        if filt and t.get("status") != filt:
            continue
        # Print a simple one-line summary for the task: id, description and status
        print("{}: {} [{}]".format(t.get("id"), t.get("description"), t.get("status")))


def cmd_update(args):
    """Update the description of a task by id.

    Usage: update 2 Buy milk and eggs
    """
    if len(args) < 2:
        print("Usage: update <id> <new description>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID must be a number")
        return
    new_desc = " ".join(args[1:])
    tasks = load_tasks()
    for t in tasks:
        if t.get("id") == tid:
            t["description"] = new_desc
            t["updatedAt"] = datetime.now().isoformat()
            try:
                save_tasks(tasks)
            except Exception:
                print("Failed to save updated task.")
                return
            print("Task {} updated".format(tid))
            return
    print("Task not found")


def cmd_delete(args):
    """Delete a task by id."""
    if not args:
        print("Usage: delete <id>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID must be a number")
        return
    tasks = load_tasks()
    # This list comprehension builds a new list that includes only tasks
    # whose id is NOT equal to `tid`. It is a concise way to filter lists.
    new = [t for t in tasks if t.get("id") != tid]
    # If the new list has the same length as the old one, nothing was removed
    # which means a task with the requested id was not found.
    if len(new) == len(tasks):
        print("Task not found")
        return
    try:
        save_tasks(new)
    except Exception:
        print("Failed to delete task (could not write file).")
        return
    print("Task {} deleted".format(tid))


def cmd_mark_done(args):
    if not args:
        print("Usage: mark-done <id>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID must be a number")
        return
    tasks = load_tasks()
    for t in tasks:
        if t.get("id") == tid:
            t["status"] = "done"
            t["updatedAt"] = datetime.now().isoformat()
            try:
                save_tasks(tasks)
            except Exception:
                print("Failed to save task status change.")
                return
            print("Task {} marked done".format(tid))
            return
    print("Task not found")


def cmd_mark_progress(args):
    if not args:
        print("Usage: mark-in-progress <id>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID must be a number")
        return
    tasks = load_tasks()
    for t in tasks:
        if t.get("id") == tid:
            t["status"] = "in-progress"
            t["updatedAt"] = datetime.now().isoformat()
            try:
                save_tasks(tasks)
            except Exception:
                print("Failed to save task status change.")
                return
            print("Task {} marked in-progress".format(tid))
            return
    print("Task not found")


def print_help():
    print("Usage: python index.py <command> [args]")
    print("Commands:")
    print("  add <description>")
    print("  list [all|todo|in-progress|done]")
    print("  update <id> <new description>")
    print("  delete <id>")
    print("  mark-done <id>")
    print("  mark-in-progress <id>")


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    cmd = sys.argv[1]
    args = sys.argv[2:]
    try:
        if cmd == "add":
            cmd_add(args)
        elif cmd == "list":
            cmd_list(args)
        elif cmd == "update":
            cmd_update(args)
        elif cmd in ("delete", "remove"):
            cmd_delete(args)
        elif cmd == "mark-done":
            cmd_mark_done(args)
        elif cmd == "mark-in-progress":
            cmd_mark_progress(args)
        else:
            print_help()
    except Exception as e:
        # Catch any unexpected error and show a friendly message instead of a traceback
        print(f"Unexpected error: {e}")
        print("If the problem persists, check file permissions or file contents of tasks.json")


if __name__ == "__main__":
    main()
