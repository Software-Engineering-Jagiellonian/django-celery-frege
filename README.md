# Fregepoc

## Perequisites

Docker & docker-compose is required to be available on the host system.

## Usage

Initially, you need to create an `.env` file following the `.env.template` template. This can be done via

```bash
cp .env.template .env
```

and then editing the `.env` file optionally (although the unchanged configuration should suffice). The former is a one-time operation.

>The following commands should be run from the **root** of the application

To run the application, you need to use the following command:

```bash
docker compose --profile application up
```

If the containers were not built yet, you can do so by running the following command:

```bash
docker compose --profile application build
```

>On older versions of Docker, you may need to substitute `docker compose` with `docker-compose`.

There exists a number of docker-compose profiles in the project, consult `docker-compose.yml` for more information.

### Linters and Formatters

The project employs a number of linters and formatters such as `flake8`, `isort`, or `black`
in order to improve the overall DX.

Also, aiming to prevent common mistakes from being committed and pushed
to the origin, one can register the git hooks configured via `pre-commit`:

```bash
pip install -r backend/requirements.txt
pre-commit install
```

Moreover, to run the linters and formatters over the entire codebase with `pre-commit`, execute the following command:
```bash
pre-commit run --all-files
```
