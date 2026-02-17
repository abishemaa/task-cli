import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    if not tasks:
        return 1
    return max(t.get("id", 0) for t in tasks) + 1


def cmd_add(args):
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
    save_tasks(tasks)
    print("Task added (ID: {})".format(task["id"]))


def cmd_list(args):
    tasks = load_tasks()
    if not args or args[0] == "all":
        filt = None
    else:
        filt = args[0]
    for t in sorted(tasks, key=lambda x: x.get("id", 0)):
        if filt and t.get("status") != filt:
            continue
        print("{}: {} [{}]".format(t.get("id"), t.get("description"), t.get("status")))


def cmd_update(args):
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
            save_tasks(tasks)
            print("Task {} updated".format(tid))
            return
    print("Task not found")


def cmd_delete(args):
    if not args:
        print("Usage: delete <id>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID must be a number")
        return
    tasks = load_tasks()
    new = [t for t in tasks if t.get("id") != tid]
    if len(new) == len(tasks):
        print("Task not found")
        return
    save_tasks(new)
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
            save_tasks(tasks)
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
            save_tasks(tasks)
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


if __name__ == "__main__":
    main()
