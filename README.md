# Python Project Checklist

یک برنامه دسکتاپ برای مدیریت چک‌لیست پروژه‌های Python.

## امکانات

- ایجاد پروژه جدید
- حذف پروژه
- تغییر نام پروژه
- نمایش چک‌لیست ۳۹ مرحله‌ای
- دسته‌بندی مراحل پروژه
- ذخیره وضعیت انجام کارها
- نمایش درصد پیشرفت پروژه
- نوار پیشرفت
- ذخیره اطلاعات در فایل JSON

## تکنولوژی‌ها

- Python
- Tkinter
- JSON

## اجرای پروژه

ابتدا محیط مجازی را فعال کنید:

```powershell
venv\Scripts\activate

سپس برنامه را اجرا کنید:

python main.py
ساختار پروژه
python_project_checklist/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── gui.py
│   ├── project_manager.py
│   └── checklist.py
│
├── data/
│   └── projects.json
│
└── tests/
    └── test_project_manager.py