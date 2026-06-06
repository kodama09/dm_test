# Final Review

This document checks the delivered project against the original assessment
instructions.

## Requirement Checklist

| Requirement | Status | Evidence |
| --- | --- | --- |
| Python language | Met | The service is a Python 3.12 package configured in `pyproject.toml`. |
| Production-oriented code quality | Met | The code is layered, typed, linted with Ruff, and covered by labelled tests. |
| FastAPI mandatory | Met | `src/bootstrap/app.py` creates the FastAPI app and registers routes. |
| Async/await patterns | Met | Use cases, routes, asyncpg repositories, migration runner, and tests use async execution. |
| FastAPI dependency injection | Met | `src/bootstrap/dependencies.py` exposes use cases with `Depends`. |
| Pydantic request/response validation | Met | HTTP schemas live under `src/presentation/schemas`. |
| Exception handlers | Met | Application errors are mapped in `src/presentation/exception_handlers`. |
| Lifespan startup/shutdown | Met | `src/bootstrap/lifespan.py` creates shared adapters, runs migrations, and closes the PostgreSQL pool. |
| No ORM | Met | Persistence uses asyncpg and raw SQL only. SQLAlchemy and Tortoise ORM are not dependencies. |
| DBMS other than SQLite | Met | PostgreSQL is the only database. SQLite is not used. |
| Email as third-party boundary | Met | Email delivery is an application port. The assessment adapter prints the activation code to the console and can be replaced by an HTTP provider. |
| Tested code | Met | Tests are split into unit, functional, integration, and regression categories. |
| Dockerized application | Met | `docker-compose.yml` starts the API and PostgreSQL. |
| Dockerized test execution | Met | `docker compose run --rm --build test` runs the full suite with only Docker installed. |
| Iterative commits | Met | The history is organized by roadmap subsection, with focused commits and feature branches. |
| Run instructions | Met | `README.md` documents application startup, API calls, and test commands. |
| Architecture schema | Met | `docs/ARCHITECTURE.md` contains component and sequence diagrams. |
| GitHub link | Ready | The final merge request will provide the reviewable GitHub link for the completed feature. |

## Functional Coverage

The implementation supports the required user lifecycle:

- Create a user with an email and password through `POST /users`.
- Generate a 4-digit numeric activation code.
- Send the activation code through the email port.
- Activate the account through `POST /users/activate` with Basic Auth and the code.
- Reject activation when the code is invalid or older than one minute.

The implementation also includes production-oriented protections:

- Email uniqueness is enforced by PostgreSQL and translated into application errors.
- Passwords are stored as PBKDF2-HMAC-SHA256 hashes.
- Activation codes are stored as HMAC-SHA256 hashes, not plaintext.
- Unknown-email activation attempts still execute dummy password verification to reduce account-enumeration timing differences.
- Startup migrations are serialized with a PostgreSQL advisory lock.
- The PostgreSQL pool is closed both on normal shutdown and startup failure.

## Database And Test Isolation

The application database is `user_registration` by default. Integration tests use
a separate `user_registration_test` database, created by the test fixtures when
PostgreSQL is available.

Before and after each integration test using PostgreSQL, the `users` table is
truncated with `RESTART IDENTITY CASCADE`. This keeps the test database stable
without altering the application database.

## Verification Commands

Primary reviewer path:

```bash
docker compose up -d --build api
curl http://localhost:8000/health
docker compose run --rm --build test
docker compose down
```

Local development checks:

```bash
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m compileall src tests
.venv\Scripts\python.exe -m pytest -v
docker compose config --quiet
```

The latest local review before this documentation pass confirmed:

- Ruff passes.
- Python compilation passes.
- The full pytest suite passes.
- Docker Compose configuration is valid.
- The Docker test service passes against PostgreSQL.
- The API container starts and `/health` returns `status: ok`.

## Remaining Scope

The console email adapter is intentionally minimal for the assessment. Replacing
it with a real third-party HTTP email provider would only require implementing
the existing `EmailSender` port and changing bootstrap wiring.

Rate limiting for activation attempts is outside the requested feature set. In a
production deployment, it should be added at the API gateway, application, or
identity-protection layer before exposing short numeric codes publicly.
