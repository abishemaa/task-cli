# Task Tracker CLI

Simple command-line task tracker.

Usage

Run commands with Python:

python index.py add "Buy groceries"
python index.py list
python index.py list done
python index.py list todo
python index.py update 1 "Buy groceries and cook dinner"
python index.py mark 1 done
python index.py mark 1 in-progress
python index.py remove 1
python index.py delete 1  # alias for remove

Task object fields stored in tasks.json:
- id: integer unique id
- description: task description
- status: todo | in-progress | done
- createdAt: ISO 8601 UTC timestamp
- updatedAt: ISO 8601 UTC timestamp

Notes
- The CLI uses positional arguments.
- The JSON file `tasks.json` is created automatically if missing.
- The application accepts legacy `not-done` status values and `task` field names for compatibility.
