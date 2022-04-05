# Fregepoc

## Perequisites

Docker & docker compose is required to be available on the host system.

## Usage

Initially, you need to create an `.env` file following the `.env.template` template. This can be done via

```bash
cp .env.template .env
```

and then editing the `.env` file optionally (although the unchanged configuration should suffice). The former is a one-time operation.

>The following commands should be run from the **root** of the application

To run the application, you need to run the following command:

```bash
docker compose --profile application up
```

If the containers were not built yet, you can do so by running the following command:

```bash
docker compose --profile application build
```

>On older versions of Docker, you may need to substitute `docker compose` with `docker-compose`.

There exists a number of docker-compose profiles in the project, consult `docker-compose.yml` for more information.
