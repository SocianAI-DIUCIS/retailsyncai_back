## RetailSyncAI Backend (Django + DRF + Elasticsearch + JWT)

RetailSyncAI Backend is a modern API layer built with Django, Django REST Framework, Elasticsearch, and JWT authentication.

### Make Sure Elasticsearch is running on http://localhost:9200

It powers the RetailSyncAI frontend and provides authentication, product indexing, searching, CRUD operations, and cross-origin access for the Next.js app.

This guide explains how to set up the backend, install dependencies, configure environment variables, run migrations, manage Elasticsearch indices, and start the development server.

### Technologies Used

- Python 3.12+
- Django (API framework)
- Django REST Framework
- Elasticsearch Python client
- djangorestframework-simplejwt (JWT authentication)
- PyJWT (token tools)
- python-dotenv (environment variables)
- django-cors-headers (CORS control)
- SQLite (default for user auth & Django tables)

### 1. Install Python & Virtual Environment

Ensure Python 3.12+ is installed:

```bash
python --version
```

Create & activate a virtual environment:
#### Clone the Project from GitHub or Download:
```bash
git clone https://github.com/SocianAI-DIUCIS/retailsyncai_back.git
```
Directly open the Project in PyCharm. It will give option to Create Virtual Environment.

#### Or for Starting the Project from Scratch:

Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Backend Requirements

Install required packages:

```bash
pip install django djangorestframework elasticsearch PyJWT python-dotenv djangorestframework-simplejwt django-cors-headers
OR
pip install -r requirements.txt
```

#### Or for Starting the Project from Scratch:

If starting from scratch:
django-admin startproject backend.

Create the API app:

```bash
python manage.py startapp api
```

### 3. Update settings.py

Add installed apps:

```bash
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",

    # Your app
    "api",
]
```

Add middleware:

```bash
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
```

Enable CORS (development mode):

```bash
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

Configure DRF default authentication:

```bash
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}
```

### 4. Environment Variables (.env)

Create a .env file inside your backend folder:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ELASTICSEARCH_HOST=http://localhost:9200
```

Load it in settings.py:

```bash
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
```

### 5. JWT Configuration

Inside settings.py, add:

```bash
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}
```

### 6. Elasticsearch Client Setup

Inside your Django app, create:

```bash
api/es_client.py:
from elasticsearch import Elasticsearch
from django.conf import settings

es = Elasticsearch(settings.ELASTICSEARCH_HOST)
```

### 7. API Endpoints Example

#### Authentication
- POST /api/auth/register/ — User registration
- POST /api/auth/login/ — Obtain access & refresh tokens
- POST /api/auth/token/refresh/ — Refresh access token

#### Products (Elasticsearch)
- POST /api/products/ — Add a product
- GET /api/products/ — List/search products (paginated)
- PUT /api/products/<id>/ — Update a product
- DELETE /api/products/<id>/ — Delete a product
- DELETE /api/products/index/ — Delete entire index
- POST /api/products/index/create/ — Create index manually

#### Articles (SQLite + Django ORM)
- POST /api/articles/
- GET /api/articles/
- PUT /api/articles/<id>/
- DELETE /api/articles/<id>/

### 8. Run Database Migrations

Apply Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Run the Development Server

Start Django API:

```bash
python manage.py runserver
```

Backend API will be live at:

http://localhost:8000/api/

### 10. Testing Elasticsearch Connection

#### Test ES availability:

```bash
from api.es_client import es
print(es.info())
```

#### If ES is running at localhost:9200, you should see cluster info.

### 11. Production Build Notes

For production:

- Set DEBUG=False
- Use a secure SECRET_KEY
 
Configure allowed hosts:

```bash
ALLOWED_HOSTS = ["your-domain.com", "localhost"]
```

Use Elastic Cloud or self-hosted Elasticsearch cluster

Setup Gunicorn + Nginx (optional)

Serve static files with collectstatic:

```bash
python manage.py collectstatic
```

You’re Ready!

Your Django backend is now fully configured with:

- REST API
- JWT authentication
- Elasticsearch
- CORS support
- Environment variables
- Django ORM models
