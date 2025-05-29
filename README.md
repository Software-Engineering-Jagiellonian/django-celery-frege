<div align="center">

![Alt text](docs/DESIGNDOC/FREGE_SIMPLE_LOGO.png)
</div>

<div align="center">
  <a href="https://github.com/Software-Engineering-Jagiellonian/django-celery-frege/issues">Check Current Tasks</a>
  ·
  <a href="https://github.com/Software-Engineering-Jagiellonian/django-celery-frege/issues/new?assignees=&labels=bug&&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/Software-Engineering-Jagiellonian/django-celery-frege/compare">Create a Pull Request</a>
</div>
<br>
<div align="center">

  ![issues](https://img.shields.io/github/issues/Software-Engineering-Jagiellonian/django-celery-frege?style=flat-square)
  ![pull-requests](https://img.shields.io/github/issues-pr/Software-Engineering-Jagiellonian/django-celery-frege?style=flat-square)

  ![license](https://img.shields.io/github/license/Software-Engineering-Jagiellonian/django-celery-frege?style=flat-square)

</div>

<details open = "open">
<summary>Table of Contents</summary>

- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Contributing](#contributing)
  - [Linters](#linters)
  - [Commit message convention](#commit-message-convention)
- [Documentation](#documentation)

</details>

# About
FREGE is an open-source application dedicated to analyzing other open-source repositories available on Github, Gitlab ect. for various metrics like average number of lines of code, average cyclomatic complexity, token count or number of devs per project.

The main goal is to gather largest database of code metrics in order to analyze them (with little help of ML) to extract hidden patterns to what makes successful project overall.

# Getting Started

## Prerequisites
Docker Desktop for your preferred system ([Linux](https://docs.docker.com/desktop/install/linux-install/)/[Windows](https://docs.docker.com/desktop/install/windows-install/)/[Mac](https://docs.docker.com/desktop/install/mac-install/)) is recommended way to get [Docker](https://docs.docker.com) with [Compose plugin](https://docs.docker.com/compose/) which are only prerequisites to run Frege project.

> :warning: When installing on Linux, please remember of [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)!

## Installation
> :warning: **Every command** needs to be run from the **root** of the project!

Follow these simple instruction to set up a development environment:

1. Create `.env` file by following `.env.template` template. Simply run:

```
cp .env.template .env
```

2. Setting up GitLab Token
- Get the token from [the following instructions](https://docs.gitlab.com/user/profile/personal_access_tokens/).
- Add the following line to the `.env` file:
```
GITLAB_TOKEN=your_token_here
```

3. Build Docker container with following command:
> :warning: On older versions of Docker, you may need to substitute docker compose with docker-compose.

```
docker compose --profile dev build
```

## Usage
Running application in **dev** environment:

```
docker compose --profile dev up
```

After running application in dev profile, check these sites:
* `localhost:3030` - front-end application
* `localhost:3000` - [Grafana](https://grafana.com/) (use search to find dashboards)
* `localhost:5555` - [Flower](https://flower.readthedocs.io/en/latest/)
* `localhost:8000` - back-end application

Running **tests** for the application:
```
docker compose exec -T frege-backend-dev pytest
```

Running application in **prod** environment (use with caution):
```
docker compose --profile prod up -d
```

# Contributing
## Linters
This project employs a number of linters and formatters for overall DX.

> :warning: To prevent common mistakes from being committed and pushed to the origin it is **highly recommended** to register git hooks configured via `pre-commit`. For this operation [pip](https://pip.pypa.io/en/stable/installation/) and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) will be needed. \
Alternatively, you can use **extensions** (such as prettier or black) to format your code in your IDE without installing anything more. However, with pip and npm already installed, pre-commit approached is more recommended.

There are three linters/formatters for Python: `flake8`, `isort`, `black`; and there are two for Javascript/TypeScript: `prettier`, `eslint`.

In order to install pre-commit git-hook, run commands (recommended with [venv](https://docs.python.org/3/library/venv.html) previously created):

1. Install python packages:

  `pip install -r backend/requirements.txt`

  For more information about development of BE please refer to [backend/README.md](backend/README.md)

2. Install npm packages:

```
cd frontend
npm install
```

To launch the application run the following command in frontend directory:

```
npm start
```

3. Install pre-commit git hook:

```
pre-commit install
```

Now, every commit will be formatted automatically. On rare occasions (such as line length) manual adjustments might be needed.

To run the linters and formatters over the entire codebase with `pre-commit`, execute the following command:

```
pre-commit run --all-files
```

## Commit message convention
In order to unify the commit messages creation strategy, it is strongly recommended adhering to [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

# Documentation

:warning: For in-depth description of the tool please refer to the [Design Document](./documentation/DESIGNDOC.md).

Some information also can be found in:
* [FrontEnd readme](./frontend/README.md)
* [Documentation readme](./documentation/README.md)
