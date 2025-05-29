#!/bin/bash

docker compose --profile profiling up --wait

docker compose exec frege-celery-worker-profiling python manage.py start_profiling

docker compose --profile profiling stop
