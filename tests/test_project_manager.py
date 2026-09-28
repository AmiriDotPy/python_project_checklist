from src.project_manager import create_project, save_project, load_projects, update_task


project = create_project("Test Project")

save_project(project)

update_task("Test Project", 0, True)

projects = load_projects()

print(projects["Test Project"]["tasks"][0])