# Task Manager

A Django-based task management application with user authentication, categories, priorities, and comments.

## Features

- User authentication (register, login, logout)
- Create, read, update, and delete tasks
- Task priorities (1-5)
- Task categories
- Task comments
- Mark tasks as complete/incomplete
- Deadline tracking
- Responsive design

## Tech Stack

- Django 5.0
- PostgreSQL
- Gunicorn
- Nginx (Docker)
- Docker & Docker Compose

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (for local development)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd task-manager
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

### Docker Setup (development)

1. Create a `.env` file (see above or copy from `.env.example`).
2. Build and run with Docker Compose:
```bash
docker compose -f docker-compose.dev.yml up --build
```
3. The application will be available at `http://localhost`

### Running Tests

```bash
pytest
```

### Production Deployment

Production uses the image built by CI and pushed to Docker Hub. On the server:

- Create a `.env.production` file with production credentials: `DOCKERHUB_USERNAME`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`, `ALLOWED_HOSTS` (use the same `DOCKERHUB_USERNAME` as the GitHub Actions secret).
- The deploy script runs `git fetch origin main && git reset --hard origin/main` in the app directory so the server has the latest files (untracked files like `.env.production` are not modified).
- Deploy with: `docker compose -f docker-compose.yml --env-file .env.production up -d`. The CI/CD workflow runs only on the `main` branch; build and deploy run only on push to `main`.

## Project Structure

```
task-manager/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/               # Main application
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── registration/
│   └── tasks/
├── static/              # Static files
│   └── css/
├── nginx/               # Nginx configuration
├── Dockerfile
├── docker-compose.yml       # production
├── docker-compose.dev.yml   # development
├── gunicorn.conf.py
└── requirements.txt
```

