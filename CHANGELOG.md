# Changelog

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
