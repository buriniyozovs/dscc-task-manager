#!/bin/bash
set -e

echo "Starting deployment..."

echo "Pulling latest images..."
docker-compose -f docker-compose.yml --env-file .env.production pull

echo "Stopping old containers..."
docker-compose -f docker-compose.yml --env-file .env.production down

echo "Building and starting new containers..."
docker-compose -f docker-compose.yml --env-file .env.production up -d

echo "Waiting for database to be ready..."
sleep 5

echo "Running migrations..."
docker-compose -f docker-compose.yml --env-file .env.production exec -T web python manage.py migrate --noinput

echo "Collecting static files..."
docker-compose -f docker-compose.yml --env-file .env.production exec -T web python manage.py collectstatic --noinput

echo "Deployment complete!"
