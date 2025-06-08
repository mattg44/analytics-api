# FastAPI Example

This project is an **example** API built with Python and SQLModel. It demonstrates a basic backend setup, including database session management and containerized deployment.

## Project Purpose

> **Note:** This repository is for **example purposes only**. It is intended to illustrate basic practices for structuring a Python API project, database session handling, and containerization.

## How It Works

- The API is built using Python, SQLModel, and FastAPI.
- Database sessions are managed via a utility in `src/api/db/session.py`.
- The application is containerized using Docker, running with Uvicorn as the ASGI server.
- **Dependency management is handled with [uv](https://github.com/astral-sh/uv) for fast and reproducible Python installs.**
- **Live reload is enabled using Docker Compose's `watch` feature, so any changes made to the local codebase are automatically reflected in the running container.**

## Running with Docker

The project includes a `Dockerfile` that sets up the environment, manages dependencies with uv, and runs the API using Uvicorn.

**Example Dockerfile snippet:**
```dockerfile
FROM python:3.13-slim

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
...
```

- The API will be available at `http://localhost:8002` when the container is running.

## Running with Docker Compose

A `docker-compose.yml` file is provided to simplify running the API and its dependencies (such as a database).
Additionally, a `pgadmin` image is included to allow admin actions on the database through a web interface.

**Example docker-compose.yml snippet:**
```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/analytics
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: analytics
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
```

- Start everything with:
  ```sh
  docker compose watch
  ```
  > **Note:** With `docker compose watch`, any changes you make to the local code will be automatically synced and reflected live in the running container.
- The pgAdmin interface will be available at `http://localhost:5050` for database administration tasks and lookup.

## Notes

- Make sure to set the `DATABASE_URL` environment variable as required by the application.
- This project is not intended for production use. .env files are included.

---

