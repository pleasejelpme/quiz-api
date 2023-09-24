#!/bin/bash

echo "### Applying migrations ###"
python manage.py makemigrations
echo "================================================================================="

echo "### Migrating ###"
python manage.py migrate
echo "================================================================================="

echo "### Runserver ###"
python manage.py runserver 0.0.0.0:8000
