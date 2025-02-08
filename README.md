# HRK Django + Docker App

![CI](https://hra-dev.vercel.app/assets/logo_hrktech_small.png)

This project serves as a base for your HRK application or as a guide to Dockerize your existing Django app.

The app is minimal but includes several features you might use in a real-world Django app without being overloaded with personal opinions.

For the Docker setup, everything included follows [Docker best practices](https://nickjanetakis.com/blog/best-practices-around-production-ready-web-apps-with-docker-compose) based on extensive experience.

**This app uses Django 5.1.2 and Python 3.13.0**.

[![Screenshot](https://raw.githubusercontent.com/designermanjeets/hra-django/refs/heads/main/assets/static/images/HRK.png)

## Table of contents

- [Tech stack](#tech-stack)
- [Notable opinions and extensions](#notable-opinions-and-extensions)
- [Running this app](#running-this-app)
- [Files of interest](#files-of-interest)
  - [`.env`](#env)
  - [`run`](#run)
- [Running a script to automate renaming the project](#running-a-script-to-automate-renaming-the-project)
- [Updating dependencies](#updating-dependencies)
- [See a way to improve something?](#see-a-way-to-improve-something)
- [Additional resources](#additional-resources)
  - [Learn more about Docker and Django](#learn-more-about-docker-and-django)
  - [Deploy to production](#deploy-to-production)
- [About the author](#about-the-author)

## Tech stack

If you don't like some of these choices, you can swap them out for something else.

### Back-end

- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://github.com/celery/celery)

### Front-end

- [esbuild](https://esbuild.github.io/)
- [TailwindCSS](https://tailwindcss.com/)
- [Heroicons](https://heroicons.com/)

#### JavaScript Libraries

- <https://hotwired.dev/>
- <https://htmx.org/>
- <https://github.com/alpinejs/alpine>
- <https://vuejs.org/>
- <https://reactjs.org/>
- <https://jquery.com/>

## Notable opinions and extensions

- **Packages and extensions**:
    - *[gunicorn](https://gunicorn.org/)* for an app server
    - *[whitenoise](https://github.com/evansd/whitenoise)* for serving static files
    - *[django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)* for request info
- **Linting and formatting**:
    - *[flake8](https://github.com/PyCQA/flake8)* for linting
    - *[isort](https://github.com/PyCQA/isort)* for sorting imports
    - *[black](https://github.com/psf/black)* for formatting
- **Django apps**:
    - `pages` app for home page
    - `up` app for health checks
- **Config**:
    - Log to STDOUT for Docker
    - Environment variables for config
    - Project directory renamed to `config/`
    - `src/config/settings.py` and `.env` for configuration
- **Front-end assets**:
    - `assets/` for CSS, JS, images, fonts
    - Custom `502.html` and `maintenance.html`
    - Modern favicons
- **Django defaults changed**:
    - Redis for cache
    - Signed cookies for session
    - `public/` for static files
    - `public_collected/` for `collectstatic`

## Running this app

You'll need [Docker installed](https://docs.docker.com/get-docker/).

#### Clone this repo and move into the directory:

```sh
git clone https://github.com/yourusername/hrk-django-app hrkapp
cd hrkapp
```

#### Copy an example .env file:

```sh
cp .env.example .env
```

#### Build everything:

```sh
docker compose up --build
```

#### Setup the initial database:

```sh
./run manage migrate
```

#### Check it out in a browser:

Visit <http://localhost:8000>.

#### Linting the code base:

```sh
./run lint
```

#### Sorting Python imports:

```sh
./run format:imports
```

#### Formatting the code base:

```sh
./run format
```

#### Running the test suite:

```sh
./run manage test
```

#### Stopping everything:

```sh
docker compose down
```

## Files of interest

### `.env`

This file is ignored from version control. It contains environment variables for configuration.

### `run`

A shell script with functions to interact with the project. Run `./run` for a list of commands.

## Running a script to automate renaming the project

#### Run the rename-project script:

```sh
bin/rename-project myapp MyApp
```

## Updating dependencies

#### In development:

```sh
./run pip3:outdated
./run yarn:outdated
./run pip3:install
./run yarn:install
```

#### In CI:

Run `docker compose build`.

#### In production:

Run `docker compose build` as part of your deploy pipeline.

## See a way to improve something?

Open an issue or start a PR.

## Additional resources

### Learn more about Docker and Django

- <https://docs.docker.com/>
- <https://docs.djangoproject.com/en/5.1/>
