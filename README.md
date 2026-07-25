<h1 align="center" style="font-weight: bold;">Neo Gaming (Backend) 🎮</h1>

<p align="center">
 <a href="#tech">Technologies</a> • 
 <a href="#started">Getting Started</a> 
</p>

<p align="center">
    <b>API service for Neo Gaming front-end.</b>
</p>


<h2 id="technologies">💻 Technologies</h2>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)


<h2 id="features">✨ Features</h2>

- 👩‍🍳 **RESTful API Endpoints** serving games information, price and selling service.
- 🔐 **Secure User Authentication** managing login, registration, and token/session validation for the Neo Gaming front-end.
- 📊 **Data Management** structured database models optimized for storing games, user and sales information.

<h2 id="started">🚀 Getting Started</h2>

Follow the steps below to run the project locally.

### Prerequisites

Make sure you have installed:

- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)
- ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

### Cloning

```bash
git clone https://github.com/michaelcostaribeiro/game_store-backend.git
```
### Installing the Dependencies (Windows)
```bash
cd game_store-backend
python -m venv .venv
.venv\scripts\activate.bat
pip install -r requirements.txt
```

### Installing the Dependencies (Linux / macOS)
```bash
cd game_store-backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Create an environment file (.env) with the following information:
```
# Adapt the information as you need
MERCADO_PAGO_ACCESS_TOKEN=APP_USR-123
MERCADO_PAGO_PUBLIC_KEY=APP_USR-321
SECRET_KEY=safekey
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS(http://localhost:5173
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
```
### Creating a database on Postgres
```
# Run this command on SQL shell after logging in Postgres:
CREATE DATABASE game_store;
```
<h3>Starting</h3>

How to start the project

```bash
# Apply database migrations
python manage.py migrate

# Create a superuser for the Admin Dashboard (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

<h2>📄 License</h2>

This project is under the MIT License.
