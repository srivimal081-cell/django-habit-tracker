# Habit Tracker – Django Web Application

A web-based Habit Tracker application developed using Python and Django. The application helps users create, manage, search, and monitor their habits, with additional features for authentication, data export, and data encryption.

## Features

- **Habit Management:** Create, view, update, and delete habits.
- **User Authentication:** Token-based authentication.
- **Database Management:** Store habit information using Django ORM and SQLite.
- **Habit Search:** Search for existing habits.
- **Data Export:** Export habit data.
- **Data Encryption:** Encrypt and decrypt stored data using Fernet cryptography.
- **Web Interface:** Django templates for interacting with the application.

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Cryptography (Fernet)

## Project Structure

```text
Habit-Tracker/
│
├── Habit/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tests/
├── crypto_utils.py
├── test_crypto.py
├── manage.py
├── main.tex
└── documentation.pdf
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Habit-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install django cryptography
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the following address in your browser:

```text
http://127.0.0.1:8000/
```

## Learning Outcomes

Through this project, I gained practical experience in:

- Python backend development.
- Django application development.
- Database operations using Django ORM.
- Implementing token-based authentication.
- Handling data using JSON.
- Data encryption and decryption.
- Building and testing web application functionality.

## Author

**Sri Vimal Sanmugam**

Bachelor's Degree in Informatics  
Technical University of Košice

---

*This project was developed as part of my programming studies to gain practical experience in backend web development and data security.*
