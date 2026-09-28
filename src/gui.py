import tkinter as tk
from tkinter import ttk, messagebox
from src.project_manager import create_project, save_project, load_projects, update_task, delete_project, rename_project

def start_gui():
    window = tk.Tk()

    window.title("Python Project Checklist")
    window.geometry("800x600")

    title_label = tk.Label(
        window,
        text="Python Project Checklist",
        font=("Arial", 20)
    )
    title_label.pack(pady=20)
    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    

    def create_new_project():
        project_name = project_entry.get()

        if project_name:
            projects = load_projects()

            if project_name in projects:
                messagebox.showwarning(
                "پروژه تکراری",
                "پروژه‌ای با این نام قبلاً وجود دارد."
    )
                return

            project = create_project(project_name)
            save_project(project)

            
            projects_list.insert(tk.END, project_name)

            projects_list.selection_clear(0, tk.END)
            projects_list.selection_set(tk.END)
            projects_list.event_generate("<<ListboxSelect>>")

            project_entry.delete(0, tk.END)


    def delete_selected_project():
        selection = projects_list.curselection()

        if not selection:
            messagebox.showwarning(
                "انتخاب پروژه",
                "لطفاً ابتدا یک پروژه را انتخاب کنید."
            )
            return

        project_name = projects_list.get(selection[0])

        confirm = messagebox.askyesno(
            "حذف پروژه",
            f"آیا مطمئن هستید که می‌خواهید پروژه «{project_name}» را حذف کنید؟"
        )

        if not confirm:
            return

        delete_project(project_name)

        projects_list.delete(selection[0])

        remaining_projects = projects_list.size()

        if remaining_projects > 0:
            new_index = min(selection[0], remaining_projects - 1)

            projects_list.selection_set(new_index)
            projects_list.activate(new_index)
            projects_list.event_generate("<<ListboxSelect>>")

        else:
            for widget in tasks_frame.winfo_children():
                widget.destroy()

            progress_label.config(
                text="پیشرفت: 0 / 39 (0%)"
            )

        progress_bar["value"] = 0
    

    def rename_selected_project():
        selection = projects_list.curselection()

        if not selection:
            messagebox.showwarning(
                "انتخاب پروژه",
                "لطفاً ابتدا یک پروژه را انتخاب کنید."
            )
            return

        old_name = projects_list.get(selection[0])
        new_name = project_entry.get().strip()

        if not new_name:
            messagebox.showwarning(
                "نام پروژه",
                "لطفاً نام جدید پروژه را وارد کنید."
            )
            return

        if new_name == old_name:
            return

        if not rename_project(old_name, new_name):
            messagebox.showwarning(
                "نام تکراری",
                "پروژه‌ای با این نام قبلاً وجود دارد."
            )
            return

        projects_list.delete(selection[0])
        projects_list.insert(selection[0], new_name)

        projects_list.selection_set(selection[0])
        projects_list.activate(selection[0])
        project_entry.delete(0, tk.END)

    
    projects_frame = tk.Frame(main_frame, width=220)
    projects_frame.pack(
        side="right",
        fill="y",
        padx=(10, 0)
    )
    projects_frame.pack_propagate(False)

    project_entry = tk.Entry(
        projects_frame,
        width=25
    )
    project_entry.pack(pady=5)

    create_button = tk.Button(
        projects_frame,
        text="ایجاد پروژه",
        command=create_new_project
    )
    create_button.pack(pady=5)

    delete_button = tk.Button(
        projects_frame,
        text="حذف پروژه",
        command=delete_selected_project
    )
    delete_button.pack(pady=5)

    rename_button = tk.Button(
    projects_frame,
    text="تغییر نام پروژه",
    command=rename_selected_project
    )
    rename_button.pack(pady=5)

    projects_label = tk.Label(
        projects_frame,
        text="پروژه‌ها",
        font=("Arial", 14, "bold")
    )
    projects_label.pack(pady=5)

    projects_list = tk.Listbox(
        projects_frame,
        width=20    ,
        height=20
    )
    projects_list.pack(fill="y", expand=True)

    projects = load_projects()

    for project_name in projects:
        projects_list.insert(tk.END, project_name)
    
    





    tasks_container = tk.Frame(main_frame)
    tasks_container.pack(pady=20, fill="both", expand=True)

    progress_label = tk.Label(
        tasks_container,
        text="پیشرفت: 0 / 39 (0%)",
        font=("Arial", 12, "bold")
    )
    progress_label.pack(anchor="e", pady=5)



    progress_bar = ttk.Progressbar(
        tasks_container,
        orient="horizontal",
        length=300,
            mode="determinate"
    )

    progress_bar.pack(anchor="e", pady=5)

    
    canvas = tk.Canvas(tasks_container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(
        tasks_container,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    tasks_frame = tk.Frame(canvas)

    canvas_window = canvas.create_window(
        (0, 0),
        window=tasks_frame,
        anchor="nw"
    )
    tasks_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
   )
    canvas.bind(
    "<Configure>",
    lambda event: canvas.itemconfig(
        canvas_window,
        width=event.width
    )
)






    def show_project(event):
        selection = projects_list.curselection()

        if not selection:
            return

        project_name = projects_list.get(selection[0])
        projects = load_projects()
        project = projects[project_name]


        completed_count = sum(
            1 for task in project["tasks"]
            if task["completed"]
        )

        total_count = len(project["tasks"])

        progress_percent = int(
            (completed_count / total_count) * 100
        )

        progress_label.config(
            text=f"پیشرفت: {completed_count} / {total_count} ({progress_percent}%)"
        )
        progress_bar["value"] = progress_percent

        for widget in tasks_frame.winfo_children():
            widget.destroy()





        current_category = None

        for index, task in enumerate(project["tasks"]):

            if task["category"] != current_category:
                current_category = task["category"]

                category_label = tk.Label(
                    tasks_frame,
                    text=current_category,
                    font=("Arial", 14, "bold"),
                    anchor="e",
                    justify="right"
                )

                category_label.pack(anchor="w", pady=(10, 5))

            task_var = tk.BooleanVar(value=task["completed"])

            def on_task_change(index=index, var=task_var):
                update_task(project_name, index, var.get())

                projects = load_projects()
                project = projects[project_name]

                completed_count = sum(
                    1 for task in project["tasks"]
                    if task["completed"]
                )

                total_count = len(project["tasks"])

                progress_percent = int(
                    (completed_count / total_count) * 100
                )

                progress_label.config(
                    text=f"پیشرفت: {completed_count} / {total_count} ({progress_percent}%)"
                )
                progress_bar["value"] = progress_percent
            
            checkbox = tk.Checkbutton(
                tasks_frame,
                text=task["title"],
                variable=task_var,
                command=on_task_change,
                anchor="e",
                justify="right"
            )

            checkbox.pack(anchor="w")





    projects_list.bind("<<ListboxSelect>>", show_project)
    window.mainloop()