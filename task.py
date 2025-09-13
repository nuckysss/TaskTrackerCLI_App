import json
import os
import datetime
import sys
import argparse

class Task:
    def __init__(self, id, description, status, createdAt, updatedAt):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            description=data["description"],
            status=data["status"],
            createdAt=data["createdAt"],
            updatedAt=data["updatedAt"]
        )

#create parser
parser = argparse.ArgumentParser(description="Task Tracker CLI")

#parse the expected command arguments(sys.argv[1])
parser.add_argument("command", choices =["add", "update", "delete", "list","list done", "list todo", "list in-progress", "mark-in-progress", "mark-done"], help="Action to perfom")
#parse the expected parameter argmuments (sys.argv[2])
parser.add_argument("params", nargs="*", help= "Parameters for the command")

args = parser.parse_args()

#print the commands that were typed into the CLI
print(args.command)
print(args.params)

def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            return [Task.from_dict(task) for task in data if isinstance(task, dict)]
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)

def add(tasks):
    if not args.params or len(args.params) < 1:
        print("Description is required to add a task.")
        return
    description = args.params[0]
    idNum = max([task.id for task in tasks], default=0) + 1
    now = datetime.datetime.now().isoformat()
    new_task = Task(idNum, description, "todo", now, now)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {idNum})")

def update(tasks):
    if not args.params or len(args.params) < 2:
        print("ID number and description are required to update a task.")
        return
    try:
        idNum = int(args.params[0])
    except ValueError:
        print("ID must be an integer.")
        return
    description = args.params[1]
    for task in tasks:
        if task.id == idNum:
            task.description = description
            task.updatedAt = datetime.datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {idNum}) updated successfully.")
            return
    print(f"Task (ID: {idNum}) not found.")

def delete(tasks):
    if not args.params or len(args.params) < 1:
        print("ID number is required to delete a task.")
        return
    try:
        idNum = int(args.params[0])
    except ValueError:
        print("ID must be an integer.")
        return
    for i, task in enumerate(tasks):
        if task.id == idNum:
            tasks.pop(i)
            save_tasks(tasks)
            print(f"Task (ID: {idNum}) deleted successfully.")
            return
    print(f"Task (ID: {idNum}) not found.")

def list_tasks(tasks):
    if args.params and len(args.params) >= 1:
        listed = [task for task in tasks if task.status == args.params[0]]
    else:
        listed = tasks
    if not listed:
        print("No tasks found.")
    else:
        for task in listed:
            print(f"ID: {task.id} | Description: {task.description} | Status: {task.status} | Created: {task.createdAt} | Updated: {task.updatedAt}")

def mark_in_progress(tasks):
    if not args.params or len(args.params) < 1:
        print("ID number is required to mark a task as in-progress.")
        return
    try:
        idNum = int(args.params[0])
    except ValueError:
        print("ID must be an integer.")
        return
    for task in tasks:
        if task.id == idNum:
            task.status = "in-progress"
            task.updatedAt = datetime.datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {idNum}) marked as in-progress.")
            return
    print(f"Task (ID: {idNum}) not found.")

def mark_done(tasks):
    if not args.params or len(args.params) < 1:
        print("ID number is required to mark a task as done.")
        return
    try:
        idNum = int(args.params[0])
    except ValueError:
        print("ID must be an integer.")
        return
    for task in tasks:
        if task.id == idNum:
            task.status = "done"
            task.updatedAt = datetime.datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {idNum}) marked as done.")
            return
    print(f"Task (ID: {idNum}) not found.")

def main():
    tasks = load_tasks()
    if args.command == "add":
        add(tasks)
    elif args.command == "update":
        update(tasks)
    elif args.command == "delete":
        delete(tasks)
    elif args.command == "list":
        list_tasks(tasks)
    elif args.command == "list done":
        args.params = ["done"]
        list_tasks(tasks)
    elif args.command == "list todo":
        args.params = ["todo"]
        list_tasks(tasks)
    elif args.command == "list in-progress":
        args.params = ["in-progress"]
        list_tasks(tasks)
    elif args.command == "mark-in-progress":
        mark_in_progress(tasks)
    elif args.command == "mark-done":
        mark_done(tasks)

if __name__ == "__main__":
    main()