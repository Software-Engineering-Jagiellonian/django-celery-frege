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

If the containers were not built yet, you can do so by running the following command:

```bash
docker compose --profile dev build
```

To run the application, you need to use the following command:

```bash
docker compose --profile dev up
```

For the production environment, use the following instead:

```bash
docker compose --profile prod up -d
```

>On older versions of Docker, you may need to substitute `docker compose` with `docker-compose`.

There exists a number of docker-compose profiles in the project, consult `docker-compose.yml` for more information.

### Linters and Formatters

The project employs a number of linters and formatters such as `flake8`, `isort`, or `black`
in order to improve the overall DX.

Also, to prevent common mistakes from being committed and pushed
to the origin, it is required to register the git hooks configured via `pre-commit`:

>One might want to create a virtual environment (e.g. `venv`, `virtualenv`, conda) before executing commands below.

```bash
pip install -r backend/requirements.txt
pre-commit install
```

Moreover, to explicitly run the linters and formatters over the entire codebase with `pre-commit`, execute the following command:
```bash
pre-commit run --all-files
```

### Testing
To run tests from the docker container, execute the following command:
```bash
docker compose exec -T fregepoc-backend pytest
```

### Commit messages convention

In order to unify the commit messages creation strategy, we strongly recommend adhering to [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).
