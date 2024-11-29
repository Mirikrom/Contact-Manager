# Contacts Management System

A Django-based contact management system with user authentication, contact and group management, and a modern UI using Tailwind CSS.

## Features
- User Registration and Authentication
- Contact Management (Create, Search, Delete)
- Group Management (Create, Search)
- Add Contacts to Groups
- Pagination
- Modern UI with Tailwind CSS
- AJAX operations using Axios

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Install Tailwind CSS dependencies:
```bash
python manage.py tailwind install
```

5. Run the development server:
```bash
python manage.py runserver
```

## Technologies Used
- Django 4.2.7
- Tailwind CSS
- Axios for AJAX operations
- Django Crispy Forms with Tailwind
