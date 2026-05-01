python := ".venv/bin/python"

run:
    {{python}} manage.py runserver

migrate:
    {{python}} manage.py migrate

makemigrations:
    {{python}} manage.py makemigrations

superuser:
    {{python}} manage.py createsuperuser