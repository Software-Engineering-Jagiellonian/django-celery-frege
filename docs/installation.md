# Installation

This document describes how to install and set up the Frege application.

---

## Prerequisites

Frege uses Docker and Docker Compose to manage services. Before starting, install Docker Desktop for your system:

- [Linux installation](https://docs.docker.com/desktop/install/linux-install/)
- [Windows installation](https://docs.docker.com/desktop/install/windows-install/)
- [macOS installation](https://docs.docker.com/desktop/install/mac-install/)

> ⚠️ **Linux users:** Don’t forget to follow Docker’s [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to allow running Docker as a non-root user.

---

## Setup

> All commands should be run from the **root directory** of the project.

### 1. Copy environment configuration

Create the `.env` file by copying the provided template:

```bash
cp .env.template .env
```

### 2. Set up GitLab token

Generate a GitLab personal access token by following [these instructions](https://docs.gitlab.com/user/profile/personal_access_tokens/).

Then, add the token to your `.env` file:

```env
GITLAB_TOKEN=your_token_here
```

### 3. Build Docker containers

Run the following command to build the containers for development:

```bash
docker compose --profile dev build
```

> 💡 On older Docker versions, replace `docker compose` with `docker-compose`.

---

Frege is now ready to run! See [Usage](./usage.md) for how to launch the application.