#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Migrate database (if needed)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
