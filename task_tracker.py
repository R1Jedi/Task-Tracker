import os
import json
import sys
from datetime import datetime

DB_FILE = "tasks.json"


def load_tasks() -> list:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: list):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def find_task(tasks: list, task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    print(f"Задача с ID {task_id} не найдена")
    sys.exit(1)


def add_task(title: str):
    tasks = load_tasks()
    task_id = tasks[-1]["id"] + 1 if tasks else 1

    new_task = {
        "id": task_id,
        "description": title,
        "status": "todo",
        "createdAt": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "updatedAt": None
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Задача успешно добавлена с ID {task_id}!")


def update_task(task_id: int, title: str):
    tasks = load_tasks()

    task = find_task(tasks, task_id)
    task["description"] = title
    task["updatedAt"] = datetime.now().strftime("%d.%m.%Y %H:%M")

    save_tasks(tasks)

    print(f"✅ Задача успешно обновлена с ID {task_id}!")
    return


def delete_task(task_id: int):
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)

            save_tasks(tasks)

            print(f"✅ Задача успешно удалена с ID {task_id}!")
            return

    print(f"Задача с ID {task_id} не найдена")
    sys.exit(1)


def mark_task(task_id: int, status: str):
    if status not in ["todo", "in-progress", "done"]:
        print(f"Статус {status} некорректный (допустимые значения [in-progress, done])")
        sys.exit(1)

    tasks = load_tasks()
    task = find_task(tasks, task_id)
    task["status"] = status
    task["updatedAt"] = datetime.now().strftime("%d.%m.%Y %H:%M")

    save_tasks(tasks)

    print(f"Статус задачи с ID {task_id} обновлен до {status}")
    return


def get_tasks(status: str | None = None) -> list:
    tasks = load_tasks()
    filter_tasks = []

    if status:
        for task in tasks:
            if task["status"] == status:
                filter_tasks.append(task)

        return filter_tasks

    return tasks


def main():
    args = sys.argv[1:]

    if not args:
        print("Ошибка: не указана команда.")
        sys.exit(1)

    command = args[0]

    if command == "add":
        if len(args) < 2:
            print("Ошибка: не указано название задачи.")
            sys.exit(1)

        title = args[1]

        add_task(str(title))

    if command == "update":
        if len(args) < 3:
            print("Ошибка: не указаны параметры (ID, title).")
            sys.exit(1)

        task_id = args[1]

        if not task_id.isdigit():
            print("Ошибка: ID задачи должен быть числом.")
            sys.exit(1)

        title = args[2]

        update_task(int(task_id), str(title))

    if command == "delete":
        if len(args) < 2:
            print("Ошибка: не указан ID задачи для удаления.")
            sys.exit(1)

        task_id = args[1]
        if not task_id.isdigit():
            print("Ошибка: ID задачи должен быть числом.")
            sys.exit(1)

        delete_task(int(task_id))

    if command == "mark":
        if len(args) < 3:
            print("Ошибка: не указан ID задачи для удаления.")
            sys.exit(1)

        task_id = args[1]
        if not task_id.isdigit():
            print("Ошибка: ID задачи должен быть числом.")
            sys.exit(1)

        status = args[2]

        mark_task(int(task_id), str(status))

    if command == "list":
        if len(args) >= 2:
            status = args[1]
            if status not in ["todo", "in-progress", "done"]:
                print(f"Ошибка: некорректный статус '{status}'. Допустимые: todo, in-progress, done")
                sys.exit(1)
        else:
            status = None

        print(get_tasks(status))


if __name__ == "__main__":
    main()

