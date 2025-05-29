## FREGE Backend

### Celery logger verbosity

You can configure verbosity of Celery workers with the environmental variable `CELERY_LOG_LEVEL_DEV` and
`CELERY_LOG_LEVEL_PROD` in your `.env` file.
Available levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `FATAL`.
Read more in the [docs](https://docs.celeryq.dev/en/stable/reference/cli.html#cmdoption-celery-worker-l).

### Redis task persistence

Resis is a task broker for Celery. It stores the long-term task queue for Celery and the Celery workers fetch
tasks from Redis when available. The task queue can persist between sessions, i.e. all tasks will be
saved on the disk when FREGE is shut down and they will be restored when FREGE is started again.
Currently it's not known whether task persistence is safe for FREGE, so it's disabled by default. You can enable it
by setting the environmental variable `REDIS_PERSISTENCE_ENABLED=True`.
