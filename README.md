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

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. The application will be available at `http://localhost`

### Running Tests

```bash
pytest
```

### Production Deployment

Production uses the image built by CI and pushed to Docker Hub. On the server, deployment runs with the production Compose override:

- Ensure the app directory (e.g. `/app/dscc-task-manager`) contains `docker-compose.prod.yml` (e.g. by pulling the repo).
- Add `DOCKERHUB_USERNAME=<your-dockerhub-username>` to the server `.env` (use the same value as the GitHub Actions secret).

The deploy job uses `docker-compose -f docker-compose.yml -f docker-compose.prod.yml` so the server pulls and runs the Hub image instead of rebuilding from local files. The CI/CD workflow runs only on the `main` branch (push and pull requests targeting main); build and deploy run only on push to `main`, so pushes to other branches (e.g. staging) do not trigger deployment.

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
├── docker-compose.yml
├── docker-compose.prod.yml
├── gunicorn.conf.py
└── requirements.txt
```

## License

MIT License
