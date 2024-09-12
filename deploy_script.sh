#!/bin/bash

DRY_RUN=$1

echo "Change directory to repo..."
if [ "$DRY_RUN" != "true" ]; then
    cd /home/ubuntu/online-book-store || { echo "Error: Failed to change directory."; exit 1; }
fi

echo "Current directory: $(pwd)"

echo "Pulling latest code from repository..."
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ "$BRANCH" == "master" ] || [ "$BRANCH" == "main" ]; then
    if [ "$DRY_RUN" != "true" ]; then
        git pull origin "$BRANCH" || { echo "Error: Failed to pull from repository."; exit 1; }
    fi
else
    echo "Error: Current branch is not master or main."
    exit 1
fi

echo "Installing dependencies..."
if [ "$DRY_RUN" != "true" ]; then
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate || { echo "Error: Failed to activate virtual environment."; exit 1; }
    else
        echo "Error: Virtual environment not found."
        exit 1
    fi

    if command -v pip &> /dev/null; then
        pip install -r requirements.txt || { echo "Error: Failed to install dependencies."; exit 1; }
    else
        echo "Error: pip not found."
        exit 1
    fi
fi

echo "CD to source..."
cd /home/ubuntu/online-book-store/src || { echo "Error: Failed to change directory."; exit 1; }

echo "Running migrations..."
if [ "$DRY_RUN" != "true" ]; then
    if command -v python &> /dev/null; then
        python manage.py migrate || { echo "Error: Failed to run migrations."; exit 1; }
    else
        echo "Error: python not found."
        exit 1
    fi
fi

echo "Restarting the server..."
if [ "$DRY_RUN" != "true" ]; then
    sudo systemctl restart gunicornSK || { echo "Error: Failed to restart server."; exit 1; }
fi

echo "Deployment complete."
