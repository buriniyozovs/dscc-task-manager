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
- PostgreSQL

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/buriniyozovs/dscc-task-manager.git
cd dscc-task-manager
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
cp .env
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

2. The application will be available at `http://localhost:8000`

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
├── .github/
│ └── workflows/
│ └── deploy.yml # CI/CD pipeline
├── config/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── tasks/ # Main application
│ ├── migrations/
│ ├── admin.py
│ ├── apps.py
│ ├── context_processors.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── templates/
│ ├── base.html
│ ├── landing.html
│ ├── registration/
│ │ ├── login.html
│ │ └── register.html
│ ├── tasks/
│ │ ├── task_list.html
│ │ ├── task_detail.html
│ │ ├── task_form.html
│ │ └── task_confirm_delete.html
│ └── categories/
│ ├── category_list.html
│ └── category_form.html
├── static/
│ └── css/
│ └── style.css
├── nginx/
│ └── nginx.conf
├── manage.py
├── Dockerfile
├── docker-compose.yml       # production
├── docker-compose.dev.yml   # development
├── gunicorn.conf.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required in production) |
| `DEBUG` | Enable debug mode (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `taskmanager` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `postgres` |
| `DB_HOST` | PostgreSQL host | `localhost` (or `db` in Docker) |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DOCKERHUB_USERNAME` | Docker Hub username (for production image) | (set on server) |

<img width="1920" height="977" alt="image" src="https://github.com/user-attachments/assets/7889f707-9a9f-4ff5-91d8-11e44fe924f7" />



