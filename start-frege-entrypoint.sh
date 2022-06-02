#!/usr/bin/bash

echo "User $(whoami) is starting frege"

sh -c "python manage.py migrate --noinput
&& python manage.py initadmin
&& python manage.py collectstatic --noinput
&& gunicorn fregepoc.wsgi:application --bind 0.0.0.0:${DOCKER_BACKEND_PORT}"