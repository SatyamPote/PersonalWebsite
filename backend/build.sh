#!/usr/bin/env bash
# This script will exit immediately if any command fails
set -o errexit

# Step 1: Upgrade pip and install all packages from requirements.txt
# This is the MOST IMPORTANT step. It installs Django, Gunicorn, etc.
pip install --upgrade pip
pip install -r requirements.txt

# Step 2: Run database migrations
# This prepares your database schema.
python manage.py migrate

# Step 3: Run collectstatic
# This gathers all static files (for the admin panel) into one folder.
python manage.py collectstatic --no-input