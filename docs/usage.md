# Usage

This document describes how to run and test the Frege application in different environments.

---

## Development Mode

To start the application in development mode, run:

```bash
docker compose --profile dev up
```

This will launch all required services. After startup, visit the following URLs:

- Frontend: [http://localhost:3030](http://localhost:3030)
- Grafana: [http://localhost:3000](http://localhost:3000)
- Flower (Celery monitoring): [http://localhost:5555](http://localhost:5555)
- Backend (Django): [http://localhost:8000](http://localhost:8000)

---

## Running Tests

To run backend tests using `pytest`, execute:

```bash
docker compose exec -T frege-backend-dev pytest
```

> Make sure the containers are already running before executing this command.

---

## Production Mode

> ⚠️ Use with caution.

To launch Frege in production mode:

```bash
docker compose --profile prod up -d
```

This will start the services in detached mode.