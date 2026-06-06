# User Registration API

Production-oriented user registration and activation API built for the
Dailymotion technical assessment.

The service lets a user register with an email and password, receive a 4-digit
activation code through a replaceable email provider, and activate the account
with Basic Auth plus the received code. Activation codes expire after one minute.

## Requirements

- Docker
- Docker Compose

No local Python installation is required to run the application or the test suite.

## Run The Application

Build and start the API with PostgreSQL:

```bash
docker compose up -d --build api
```

The API is then available at:

```txt
http://localhost:8000
```

Check the service health:

```bash
curl http://localhost:8000/health
```

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

## Run The Tests

Run the full labelled test suite in Docker:

```bash
docker compose run --rm --build test
```

The test service uses PostgreSQL from Docker Compose and creates an isolated
`user_registration_test` database. Integration tests truncate their data before
and after each run, so they do not alter the application database.

Run one test category:

```bash
docker compose run --rm test pytest -m unit -v
docker compose run --rm test pytest -m functional -v
docker compose run --rm test pytest -m integration -v
docker compose run --rm test pytest -m regression -v
```

## API Endpoints

### GET /health

Returns application metadata and health status.

Example response:

```json
{
  "name": "user-registration-api",
  "version": "1.0.0",
  "codename": "SCL-test",
  "status": "ok"
}
```

### POST /users

Registers a pending user and sends an activation code through the email port.

Example request:

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"ada@example.com","password":"CorrectHorse123"}'
```

Example response:

```json
{
  "id": "5c8a198a-7f0d-465f-9a61-bcd343ec6435",
  "email": "ada@example.com",
  "status": "pending_activation"
}
```

The default email adapter prints the activation code in the API container logs:

```bash
docker compose logs api
```

### POST /users/activate

Activates a pending account. The email and password are provided with Basic Auth;
the activation code is provided in the JSON body.

Example request:

```bash
curl -X POST http://localhost:8000/users/activate \
  -u ada@example.com:CorrectHorse123 \
  -H "Content-Type: application/json" \
  -d '{"activation_code":"1234"}'
```

Example response:

```json
{
  "id": "5c8a198a-7f0d-465f-9a61-bcd343ec6435",
  "email": "ada@example.com",
  "status": "activated"
}
```

## Configuration

Configuration is loaded from environment variables. Defaults are suitable for
local Docker Compose execution.

| Variable | Default | Description |
| --- | --- | --- |
| `APP_ENV` | `local` | Runtime environment name. |
| `ACTIVATION_CODE_LENGTH` | `4` | Numeric activation code length, between 4 and 12 digits. |
| `ACTIVATION_CODE_SECRET` | `local_activation_code_secret` | Secret used to hash activation codes. |
| `POSTGRES_DB` | `user_registration` | Application PostgreSQL database. |
| `POSTGRES_HOST` | `postgres` in Compose | PostgreSQL host. |
| `POSTGRES_USER` | `user_registration` | PostgreSQL user. |
| `POSTGRES_PASSWORD` | `user_registration_password` | PostgreSQL password. |
| `POSTGRES_PORT` | `5432` | PostgreSQL port. |
| `POSTGRES_POOL_MIN_SIZE` | `1` | Minimum asyncpg pool size. |
| `POSTGRES_POOL_MAX_SIZE` | `10` | Maximum asyncpg pool size. |
| `POSTGRES_POOL_COMMAND_TIMEOUT` | `30.0` | asyncpg command timeout in seconds. |

`.env.example` documents the same variables. Local `.env` files are ignored.

## Architecture

The project follows Clean Architecture:

- `domain` contains entities and value objects.
- `application` contains commands, DTOs, use cases, exceptions, and ports.
- `presentation` contains FastAPI routes, request/response schemas, mappers, and
  exception handlers.
- `infrastructure` contains asyncpg persistence, security adapters, and the
  console email adapter.
- `bootstrap` wires concrete infrastructure into application use cases through
  FastAPI lifespan and dependency injection.

Business logic is kept out of FastAPI routes. Routes only validate HTTP input,
build commands, call use cases, and map DTOs to responses.

See `docs/ARCHITECTURE.md` for the full architecture schema.

## Technical Decisions

- FastAPI is used for HTTP routing, dependency injection, Pydantic models,
  exception handlers, and lifespan startup/shutdown.
- PostgreSQL is the only database.
- asyncpg is used directly for connection pooling and SQL execution.
- No ORM is used: no SQLAlchemy, no Tortoise ORM, no SQLite, no Alembic.
- Migrations are lightweight versioned SQL files executed at startup.
- Passwords are hashed with PBKDF2-HMAC-SHA256.
- Activation codes are hashed with HMAC-SHA256 before storage.
- The email provider is an application port with a console implementation for
  the assessment; it can be replaced by an HTTP provider without changing use
  cases.

## Development Without Docker

Docker is the supported reviewer path. For local development only, install the
optional dev dependencies:

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m pytest -v
```
