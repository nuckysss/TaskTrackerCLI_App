Task Tracker CLI
Task Tracker is a simple command-line tool to manage your tasks. You can add tasks, update them, mark them as done or in-progress, and list them. Tasks are saved in a JSON file in the current folder

Features:
Add new tasks
Update or delete tasks
Mark tasks as todo, in-progress, or done
List all tasks or filter by status

Usage Examples
Add a task
task-cli add "Buy groceries"

Update a task
task-cli update 1 "Buy groceries and cook dinner"

Delete a task
task-cli delete 1

Mark a task
task-cli mark-in-progress 2
task-cli mark-done 2

List tasks
task-cli list
task-cli list todo
task-cli list in-progress
task-cli list done

Task Format
Each task in tasks.json looks like this, in a list:
{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "createdAt": "2025-09-12T10:00:00",
  "updatedAt": "2025-09-12T10:00:00"
}