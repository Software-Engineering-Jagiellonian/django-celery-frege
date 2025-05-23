#!/bin/bash

docker compose --profile profiling up --wait

PROFILING_WORKER_CONTAINER=$(docker compose ps --quiet frege-celery-worker-profiling)

docker exec "$PROFILING_WORKER_CONTAINER" python manage.py start_profiling

docker compose --profile profiling down
