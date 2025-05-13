# 📰 Press Agency Django App

## Description

**Press Agency** is a Django-based web application designed to manage newspaper publications within a press agency.
Authors (Redactors) can create topics, publish articles, and maintain personal profiles.

🌍 Live Demo
The project is available at: https://press-agency.onrender.com/

## 🔧 Features

- 🔐 User registration and authentication
- 🧑‍💼 Author profiles with biography and personal data
- 🗂️ Topic creation and filtering by the author
- 📰 Article (Newspaper) creation, listing, and search
- 🛠️ Admin panel with customized model management

## 🏗️ Tech Stack

- Python 3
- Django
- SQLite (default DB)
- HTML/CSS (Django Templates)

## 🌐 URL Routes Overview

| URL                   | Purpose                   |
|-----------------------|---------------------------|
| `/`                   | Homepage                  |
| `/accounts/login/`    | User login                |
| `/accounts/register/` | User registration         |
| `/author-profile/`    | Author profile management |
| `/newspaper-details/` | Add a newspaper article   |
| `/newspaper-list/`    | List and search articles  |
| `/topic-list/`        | List of topics            |
| `/contact-us/`        | Contact page              |
| `/about-us/`          | About the platform        |

## ▶️ Getting Started

```bash
# Clone the repository
git clone <repository_url>

# Navigate to the project directory
cd press-agency

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

## 👤 Admin Access

To create a superuser for accessing Django Admin:

```bash
python manage.py createsuperuser
```

## 📂 Models Overview

- `Redactor`: Custom user model with pen name, date of birth, experience, and autobiography.
- `Topic`: Represents a publication topic tied to a Redactor.
- `Newspaper`: Represents a newspaper article with title, content, topic, and publisher.