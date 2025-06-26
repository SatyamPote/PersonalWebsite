#!/usr/bin/env bash
# exit on error
set -o errexit

# This line installs all your packages, including Django
pip install -r requirements.txt

# This line collects static files for the admin panel
python manage.py collectstatic --no-input

# This line applies database migrations
python manage.py migrate