#!/bin/bash

DRY_RUN=$1

if [ ! -d "/home/ubuntu/online-book-store" ]; then
  echo "Directory /home/ubuntu/online-book-store does not exist."
  exit 1
fi
echo "Directory /home/ubuntu/online-book-store does not exist."
echo "Change directory to repo..."
[ "$DRY_RUN" != "true" ] && cd /home/ubuntu/online-book-store

echo "Pulling latest code from repository..."
# Skip actual git pull in dry run
[ "$DRY_RUN" != "true" ] && git pull

echo "Installing dependencies..."
# Skip actual installation in dry run
[ "$DRY_RUN" != "true" ] && source .venv/bin/activate
[ "$DRY_RUN" != "true" ] && pip install -r requirements.txt

echo "CD to source..."
cd /home/ubuntu/online-book-store/src

echo "Running migrations..."
# Skip actual migrations in dry run
[ "$DRY_RUN" != "true" ] && python manage.py migrate

echo "Restarting the server..."
# Skip actual restart in dry run
[ "$DRY_RUN" != "true" ] && sudo systemctl restart gunicornSK

echo "Deployment complete."
