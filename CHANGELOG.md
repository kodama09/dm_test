# Changelog

## 0.7.0 - Minimal tests

### 🧪 Test

• Add labelled pytest markers for unit, functional, integration, and regression tests.
• Add functional health endpoint coverage.
• Add registration use case, HTTP endpoint, duplicate email regression, and PostgreSQL repository integration coverage.
• Add activation use case, HTTP endpoint, error response regression, timing regression, and PostgreSQL activation persistence coverage.
• Run integration tests against the isolated `user_registration_test` PostgreSQL database.
• Clean integration test data with `TRUNCATE TABLE users RESTART IDENTITY CASCADE`.

### ✨ Add

• Add shared test fixtures for in-process FastAPI HTTP clients.
• Add PostgreSQL integration fixtures that create and migrate the dedicated test database.

### 🔒 Security

• Keep integration tests isolated from the application database.
• Preserve explicit PostgreSQL and asyncpg test coverage without an ORM (such as SQLAlchemy or Tortoise) or SQLite.

---

## 0.6.0 - Account activation

### ✨ Add

• Add the account activation use case for pending users.
• Add activation validation for Basic Auth credentials, activation codes, expiration, and activation status.
• Add repository support for persisting activated user state.
• Add the `POST /users/activate` route with Basic Auth and request validation.
• Add consistent API exception handlers for registration and activation errors.

### 🧪 Test

• Validate Python source compilation.
• Validate Ruff checks.
• Validate Docker Compose API and PostgreSQL services rebuild successfully.
• Validate successful registration and activation through the running API.
• Validate duplicate registration, invalid activation code, invalid credentials, expired activation code, and already activated account HTTP responses.

### 🔒 Security

• Require Basic Auth credentials for account activation.
• Verify passwords and activation codes through hashing ports.
• Keep activation errors mapped to explicit HTTP responses without exposing stored secrets.

---

## 0.5.0 - User registration

### ✨ Add

• Add the registration use case for pending user creation.
• Add password hashing, activation code generation, activation code hashing, and console email adapters.
• Add an asyncpg user repository for explicit PostgreSQL persistence.
• Add the `POST /users` route with request and response schemas.
• Wire user registration through FastAPI dependencies while keeping routes thin.

### 🧪 Test

• Validate Python source compilation.
• Validate Ruff checks.
• Validate Docker Compose API and PostgreSQL services are running.
• Validate successful `POST /users` registration through the running API.
• Validate registered users are persisted in PostgreSQL with `pending_activation` status.
• Validate activation codes are emitted through the console email adapter logs.

### 🔒 Security

• Store password hashes instead of raw passwords.
• Store activation code hashes instead of raw activation codes.
• Keep the registration workflow behind application ports for persistence, hashing, code generation, time, and email delivery.

---

## 0.4.0 - Domain and application contracts

### ✨ Add

• Add the user domain entity and activation status.
• Add email and activation code value objects.
• Add registration and activation application commands.
• Add registration and activation DTOs.
• Add application ports for persistence, email delivery, hashing, code generation, and time.

### 🧪 Test

• Validate Python source compilation.
• Validate Ruff checks.

### 🩹 Fix

• Require timezone-aware UTC datetimes for user lifecycle and activation expiration checks.

### ♻️ Refactor

• Clarify application port contracts with ellipsis method bodies.

### 🔒 Security

• Keep domain and application contracts independent from FastAPI, asyncpg, and infrastructure implementations.
• Keep activation codes represented as secrets through value objects and hashing ports.

---

## 0.3.0 - Database foundation

### ✨ Add

• Add an asyncpg PostgreSQL connection pool opened and closed through FastAPI lifespan.
• Add default local PostgreSQL settings aligned with `.env.example`.
• Add configurable PostgreSQL pool sizing and command timeout settings.
• Add the initial versioned SQL migration for the `users` table.
• Add a lightweight asyncpg migration runner executed during application startup.

### 🩹 Fix

• Provide local database settings defaults to avoid settings validation errors without a `.env` file.
• Close the PostgreSQL pool when startup migration execution fails.
• Serialize migration execution with a PostgreSQL advisory lock to avoid concurrent DDL across instances.

### 🧪 Test

• Validate Python source compilation.
• Validate Ruff checks.
• Validate Docker Compose build and startup with PostgreSQL.
• Validate migration execution and idempotent API restart.

### 🔒 Security

• Keep persistence explicit with asyncpg and raw SQL only.
• Track migrations without Alembic, SQLAlchemy, SQLite, or ORM dependencies.

---

## 0.2.0 - Configuration and runtime bootstrap

MR: [#2 - Configuration and runtime bootstrap](https://github.com/kodama09/dm_test/pull/2)

### ✨ Add

• Add cached application settings loaded with pydantic-settings.
• Add Docker Compose runtime with PostgreSQL and healthcheck.
• Add an application Dockerfile for the FastAPI service.
• Add setuptools packaging configuration for container builds.

### 📝 Docs

• Add the changelog structure.
• Document the feature finalization rule for version bumps, changelog entries, and merge request bodies.

### 🩹 Fix

• Make setuptools package installation explicit to avoid ambiguous package discovery.

### 🧪 Test

• Validate settings loading and environment override locally.
• Validate Docker Compose YAML syntax.
• Validate the health endpoint still returns application metadata.
• Validate local wheel build metadata without dependency resolution.

### 🔒 Security

• Keep local environment values out of version control through `.env`.
• Run the application container as a non-root user.

---

## 0.1.0 - Project skeleton

MR: [#1 - Project skeleton](https://github.com/kodama09/dm_test/pull/1)

### ✨ Add

• Add Python project configuration with FastAPI, Uvicorn, Pydantic, pytest, httpx, and Ruff.
• Add the Clean Architecture package structure across bootstrap, config, presentation, application, domain, and infrastructure layers.
• Add the FastAPI application factory, minimal lifespan, and `/health` endpoint.
• Add application metadata loading from `pyproject.toml`.

### 🩹 Fix

• Search upward for `pyproject.toml` instead of relying on a fixed parent depth.
• Cache application metadata loading to avoid repeated file parsing.
• Rename the unused lifespan app argument to clarify intent.

### 🧪 Test

• Validate the `/health` endpoint response locally.
• Validate Python source compilation.

### 🔒 Security

• Keep application metadata centralized in `pyproject.toml` to avoid conflicting runtime values.
