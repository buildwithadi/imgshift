#!/bin/bash
set -e

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput
