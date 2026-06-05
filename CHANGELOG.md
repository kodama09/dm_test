# Changelog

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

### 🧪 Test

• Validate settings loading and environment override locally.
• Validate Docker Compose YAML syntax.
• Validate the health endpoint still returns application metadata.

### 🔒 Security

• Keep local environment values out of version control through `.env`.

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
