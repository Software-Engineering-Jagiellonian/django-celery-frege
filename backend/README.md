### Local BE development setup

For BE development the minimal required set of services is:

- `frege-backend`
- `frege-redis`
- `frege-postgres`
- `frege-celery-crawl-worker-dev`
- `frege-celery-downloads-worker-dev`
- `frege-celery-worker-dev`

Similarly to the instruction in a main README, firstly copy `.env.template` file and save as `.env` file in root
directory of the whole FREGE repository. Next step is to modify `DJANGO_DEBUG` env variable in this file to be `True`
to avoid problems with static files in Django admin.

> **IMPORTANT!** In case of running application in production this flag has to be set to `False` to avoid memory leaks
> in celery workers!!!

1. To build application use the following command:

```
docker compose --profile local-be-dev build
```

2. Now to run application use the following command:

```
docker compose --profile local-be-dev up
```

If you would like to clean up DB and start to gather metrics from the beginning use the following commands

```
docker compose --profile local-be-dev down
docker volume prune
```

and then run app again like in section 2.

### Celery logger verbosity

You can configure verbosity of Celery workers with the environmental variable `CELERY_LOG_LEVEL_DEV` and
`CELERY_LOG_LEVEL_PROD` in your `.env` file.
Available levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `FATAL`.
Read more in the [docs](https://docs.celeryq.dev/en/stable/reference/cli.html#cmdoption-celery-worker-l).
