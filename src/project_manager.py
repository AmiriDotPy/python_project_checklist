import json
from pathlib import Path
from src.checklist import CHECKLIST

DATA_FILE = Path("data/projects.json")


def create_project(project_name):
    tasks = []

    for task in CHECKLIST:
        tasks.append({
            "category": task["category"],
            "title": task["title"],
            "completed": False
        })

    project = {
        "name": project_name,
        "tasks": tasks
    }

    return project

def save_project(project):
    projects = load_projects()

    projects[project["name"]] = project

    DATA_FILE.parent.mkdir(exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(projects, file, ensure_ascii=False, indent=4)

def load_projects():
    if not DATA_FILE.exists():
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    if not content:
        return {}

    return json.loads(content)



def update_task(project_name, task_index, completed):
    projects = load_projects()

    projects[project_name]["tasks"][task_index]["completed"] = completed

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(projects, file, ensure_ascii=False, indent=4)


def delete_project(project_name):
    projects = load_projects()

    if project_name in projects:
        del projects[project_name]

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                projects,
                file,
                ensure_ascii=False,
                indent=4
            )

def rename_project(old_name, new_name):
    projects = load_projects()

    if old_name not in projects:
        return False

    if new_name in projects:
        return False

    projects[new_name] = projects.pop(old_name)
    projects[new_name]["name"] = new_name

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            projects,
            file,
            ensure_ascii=False,
            indent=4
        )

    return True