#!/bin/bash

DRY_RUN=$1

echo "Change directory to repo..."
if [ "$DRY_RUN" != "true" ]; then
    cd /home/ubuntu/online-book-store
fi

echo "Current directory: $(pwd)"

echo "Pulling latest code from repository..."
# Check if the branch is master or main
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" == "master" ] || [ "$BRANCH" == "main" ]; then
    [ "$DRY_RUN" != "true" ] && git pull origin "$BRANCH"
else
    echo "Error: Current branch is not master or main."
    exit 1
fi

echo "Installing dependencies..."
if [ "$DRY_RUN" != "true" ]; then
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    else
        echo "Error: Virtual environment not found."
        exit 1
    fi
    if command -v pip &> /dev/null; then
        pip install -r requirements.txt
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
        python manage.py migrate
    else
        echo "Error: python not found."
        exit 1
    fi
fi

echo "Restarting the server..."
if [ "$DRY_RUN" != "true" ]; then
    sudo systemctl restart gunicornSK
fi

echo "Deployment complete."
