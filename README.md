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

1. Create a `.env` file (see above or copy from `.env.example`). Set `SSL_DOMAIN=localhost` for local HTTPS.
2. Generate dev HTTPS certificates (one-time, required for nginx in Docker):
```bash
bash scripts/generate-dev-certs.sh
```
On Windows with Git Bash or WSL, run the same script. This creates self-signed certs in `dev-certs/live/localhost/` (the folder is gitignored).
3. Build and run with Docker Compose:
```bash
docker compose -f docker-compose.dev.yml up --build
```

4. The application will be available at `https://localhost` 

### Running Tests

```bash
pytest
```

### Production Deployment

Production uses the image built by CI and pushed to Docker Hub. On the server:

- Create a `.env.production` file with production credentials: `DOCKERHUB_USERNAME`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`, `ALLOWED_HOSTS`, and `SSL_DOMAIN` (your production domain, e.g. `dscc-buriniyozov.norwayeast.cloudapp.azure.com`). Use the same `DOCKERHUB_USERNAME` as the GitHub Actions secret. HTTPS uses Let's Encrypt certs under `/etc/letsencrypt` on the server; ensure certs exist for `SSL_DOMAIN` (e.g. via `certbot certonly --standalone -d <domain>`).
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
├── app_screenshots/
│ ├── categories_list.png
│ ├── delete_task.png
│ ├── landing_page_1.png
│ ├── landing_page_2.png
│ ├── login.png
│ ├── register.png
│ ├── search_task.png
│ ├── sort_by_category.png
│ ├── sort_by_status.png
│ ├── task_create.png
│ ├── task_details.png
│ ├── task_edit.png
│ └── task_list.png
├── static/
│ └── images/
│   └── tasks-preview.png
├── nginx/
│ ├── nginx.conf
│ ├── nginx.conf.template
│ ├── entrypoint.sh
│ └── Dockerfile
├── manage.py
├── Dockerfile
├── docker-compose.yml       # production
├── docker-compose.dev.yml   # development
├── gunicorn.conf.py
├── scripts/
│ └── generate-dev-certs.sh
├── pytest.ini
├── requirements.txt
└── README.md
```

## SSL / HTTPS

- **Dev:** Set `SSL_DOMAIN=localhost` in `.env`. Certificates live under `dev-certs/live/<SSL_DOMAIN>/`; generate them once with `bash scripts/generate-dev-certs.sh`. The app is served over `https://localhost` (self-signed; accept the browser warning).
- **Prod:** Set `SSL_DOMAIN` in `.env.production` to your public domain. Nginx expects Let's Encrypt certs at `/etc/letsencrypt/live/<SSL_DOMAIN>/` on the server (mount point `/etc/nginx/ssl` in the container). Obtain certs with Certbot (e.g. `certbot certonly --standalone -d <domain>`) and ensure renewal is configured.

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
| `SSL_DOMAIN` | Domain used for SSL cert paths (dev: `localhost`, prod: your public domain) | `localhost` |

<img width="1920" height="977" alt="image" src="https://github.com/user-attachments/assets/7889f707-9a9f-4ff5-91d8-11e44fe924f7" />



