#!/bin/bash

while true; do
  # Run Pytest with variables content in fail
  docker compose exec -T frege-backend-dev pytest frege/repositories/tests/test_consumers.py --showlocals

  # Capture the exit status
  pytest_exit_status=$?

  if [ $pytest_exit_status -ne 0 ]; then
    echo "Pytest failed finally"
    exit $pytest_exit_status
  else
    echo "Pytest success, try again"
  fi
done

