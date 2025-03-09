#!/bin/sh

sh wait-for-postgres.sh db
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8008