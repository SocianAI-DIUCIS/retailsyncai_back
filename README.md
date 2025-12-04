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

### 3. For first Time, Migration and Seeding
```bash
#### python manage.py migrate_es
#### python manage.py seed_es
```


### 4. API Endpoints Example

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

### 5. Run the Development Server

Start Django API:

```bash
python manage.py runserver
```

Backend API will be live at:

http://localhost:8000/api/

### 6. Testing Elasticsearch Connection

#### Test ES availability:

```bash
from api.es_client import es
print(es.info())
```

#### If ES is running at localhost:9200, you should see cluster info.

### 7. Production Build Notes

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
