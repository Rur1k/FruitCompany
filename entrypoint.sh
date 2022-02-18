#! /bin/bash

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec uvicorn FruitCompany.asgi:application --host 0.0.0.0 --port 8000