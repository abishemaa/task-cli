# Task Tracker CLI

Simple command-line task tracker.

Usage

Run commands with Python from the project folder. Examples:

```bash
python index.py add "Buy groceries"
python index.py list
python index.py list todo
python index.py update 1 "Buy groceries and cook dinner"
python index.py mark-done 1
python index.py mark-in-progress 2
python index.py delete 1
```

Task object fields stored in tasks.json:
- id: integer unique id
- description: task description
- status: todo | in-progress | done
- createdAt: ISO 8601 UTC timestamp
- updatedAt: ISO 8601 UTC timestamp

Notes
- The CLI uses simple positional arguments (no flags).
- The JSON file `tasks.json` is created automatically if missing.
- Fields: `id`, `description`, `status`, `createdAt`, `updatedAt`.
- Status values: `todo`, `in-progress`, `done`.
