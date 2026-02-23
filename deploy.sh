#!/bin/bash
set -e

echo "Starting deployment..."

echo "Pulling latest images..."
docker-compose pull

echo "Stopping old containers..."
docker-compose down

echo "Building and starting new containers..."
docker-compose up -d --build

echo "Waiting for database to be ready..."
sleep 5

echo "Running migrations..."
docker-compose exec -T web python manage.py migrate --noinput

echo "Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "Deployment complete!"
