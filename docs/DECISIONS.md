# DECISIONS.md

## D001 — PostgreSQL is used

PostgreSQL is used as the database.

Reason:

The assessment explicitly allows choosing the DBMS but forbids SQLite. PostgreSQL is a production-grade relational database and is appropriate for this kind of API.

---

## D002 — No ORM

No ORM is used.

Reason:

The assessment explicitly forbids ORMs, including SQLAlchemy and Tortoise ORM.

The project uses explicit SQL through asyncpg.

---

## D003 — Clean Architecture

The project follows Clean Architecture / Hexagonal Architecture.

Reason:

The assessment targets a Staff Python Engineer position focused on API architecture, migration, maintainability, and technical leadership.

The architecture must show clear separation between:

- HTTP presentation.
- Application workflows.
- Domain concepts.
- Infrastructure adapters.

---

## D004 — FastAPI routes are thin

FastAPI routes only handle HTTP concerns.

Reason:

Business logic must remain testable without HTTP and without FastAPI.

Routes must delegate to application use cases.

---

## D005 — Email provider is a port

The email sender is defined as an application port and implemented as an infrastructure adapter.

Reason:

The assessment explicitly says that the SMTP/email service must be considered a third-party service.

For the test, a console email provider is acceptable.

The design allows replacing it later with an HTTP email provider without changing the use cases.

---

## D006 — Activation codes are treated as secrets

Activation codes should be hashed before storage.

Reason:

An activation code is a temporary secret.

Even if the code is short-lived, storing it hashed demonstrates a security-aware design.

---

## D007 — Basic Auth is used only for activation

Basic Auth is used for the activation endpoint.

Reason:

The assessment explicitly says Basic Auth is enough for this step.

This does not imply Basic Auth would be chosen for a complete production authentication system.

---

## D008 — Docker Compose is the default runtime

The application and PostgreSQL must run through Docker Compose.

Reason:

The assessment requires reviewers to run the project without installing anything except Docker and Docker Compose.

---

## D009 — Explicit folders are kept for repeatability

Folders such as `commands`, `dto`, `mappers`, and `services` are kept even if the project is small.

Reason:

The goal is to enforce a repeatable project structure.

They must not be filled with decorative abstractions.

They should contain code only when there is a real responsibility.

---

## D010 — Codex works one commit at a time

Codex must implement exactly one roadmap subsection per iteration.

Reason:

The assessment asks for iterative commits to understand the development reasoning.

A single large AI-generated commit would weaken the submission.


---

## D011 — Application metadata have a single source of truth

Application name, version and codename are defined only in pyproject.toml.

All services requiring these values must retrieve them programmatically.

No duplicated metadata values are allowed anywhere else in the codebase.

Version will start at 0.1.0 and codename will be SCL-test

---

## D012 — Feature finalization includes versioning and changelog

Each feature is finalized by incrementing the project version, updating the changelog, and writing the merge request.

The merge request body must be strictly equal to the text added to the changelog for that feature version.
