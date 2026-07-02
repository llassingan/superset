# Minimal Apache Superset Deployment with Docker Compose

This project provides a minimal production-oriented deployment of Apache Superset using Docker Compose.

It consists of two containers:

* **Superset** – Web application
* **PostgreSQL** – Metadata database used by Superset

The metadata database stores all application data, including:

* Users
* Roles & permissions
* Dashboards
* Charts
* Datasets
* Saved SQL
* Database connections

---

# Architecture

```
                +---------------------+
                |     Web Browser     |
                +----------+----------+
                           |
                           | HTTP (8007)
                           |
                +----------v----------+
                |      Superset       |
                |   Gunicorn Server   |
                +----------+----------+
                           |
                           | PostgreSQL
                           |
                +----------v----------+
                |     PostgreSQL      |
                | Metadata Database   |
                +---------------------+
```

---

# Project Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── requirements.txt          # Optional additional Python packages
└── superset_config.py        # Custom Superset configuration
```

---

# Services

## PostgreSQL

The PostgreSQL container stores all Superset metadata.

A named Docker volume is used:

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

This means dashboards and users remain available even if the Superset container is recreated.

---

## Superset

The Superset container is responsible for:

* Running database migrations
* Creating the initial admin user (if it does not already exist)
* Initializing Superset
* Starting the Gunicorn web server

Current startup sequence:

```text
superset db upgrade
        ↓
create admin (ignored if already exists)
        ↓
superset init
        ↓
gunicorn
```

---

# First Deployment

Build and start the services.

```bash
docker compose up -d --build
```

The first startup may take a minute while Superset initializes its metadata.

After startup, access Superset:

```
http://<server-ip>:8007
```

Default credentials:

```
Username: admin
Password: password
```

---

# Updating Superset

## Updating Python packages

If a package is added to the Dockerfile or `requirements.txt`:

```bash
docker compose up -d --build --no-deps superset
```

This rebuilds only the Superset image.

The PostgreSQL container is not restarted.

---

## Updating `superset_config.py`

Because the configuration file is mounted as a volume:

```yaml
volumes:
  - ./superset_config.py:/app/pythonpath/superset_config.py
```

Changes become available immediately on the host.

Restart the Superset container to apply them:

```bash
docker compose restart superset
```

---

# Restarting Superset

Restart only the application:

```bash
docker compose restart superset
```

This **does not restart PostgreSQL**.

During startup, the following commands execute:

```text
superset db upgrade
superset fab create-admin
superset init
gunicorn
```

These commands are designed to be idempotent.

If nothing has changed:

* Database migrations are skipped.
* Admin creation is ignored because the user already exists.
* Initialization safely refreshes permissions and metadata.
* Gunicorn starts normally.

---

# Persistent Data

All application metadata is stored inside PostgreSQL.

The following objects persist across Superset container rebuilds or restarts:

* Dashboards
* Charts
* Datasets
* Users
* Roles
* Permissions
* Database connections
* Saved SQL
* Reports
* Alerts

Recreating the Superset container does **not** remove these objects.

---

# Data Loss

The metadata will only be lost if the PostgreSQL data volume is removed.

For example:

```bash
docker compose down -v
```

or

```bash
docker volume rm postgres-data
```

Avoid using `-v` unless you intentionally want a fresh installation.

---

# Common Commands

## Start services

```bash
docker compose up -d
```

---

## Build and start

```bash
docker compose up -d --build
```

---

## Restart only Superset

```bash
docker compose restart superset
```

---

## Stop only Superset

```bash
docker compose stop superset
```

---

## Start only Superset

```bash
docker compose start superset
```

---

## View logs

```bash
docker compose logs -f superset
```

---

## View PostgreSQL logs

```bash
docker compose logs -f db
```

---

## Rebuild only Superset

```bash
docker compose up -d --build --no-deps superset
```

---

# Notes

This repository intentionally keeps initialization (`superset db upgrade`, `superset init`, and admin creation) inside the container startup command for simplicity.

Although larger production deployments often separate initialization into a dedicated one-time job, this approach is perfectly suitable for small to medium deployments because:

* Initialization commands are idempotent.
* Existing dashboards and users are preserved.
* The PostgreSQL metadata database remains untouched during Superset restarts.
* Operational complexity is minimized.

For environments with multiple Superset replicas or automated CI/CD pipelines, separating initialization into a dedicated deployment step is recommended.
