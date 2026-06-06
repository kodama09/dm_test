# Architecture

This service implements a user registration and activation API with Clean
Architecture. The central rule is that business decisions live in the domain and
application layers, while FastAPI, PostgreSQL, hashing, and email delivery remain
replaceable details.

## Component Schema

```mermaid
flowchart TD
    Client["HTTP client"]
    FastAPI["Presentation\nFastAPI routes, Pydantic schemas,\nexception handlers"]
    UseCases["Application\nRegisterUserUseCase\nActivateUserUseCase"]
    Ports["Application ports\nUserRepository, EmailSender,\nPasswordHasher, ActivationCodeHasher,\nActivationCodeGenerator, Clock"]
    Domain["Domain\nUser entity\nEmail and ActivationCode value objects"]
    Bootstrap["Bootstrap\nFastAPI app, lifespan,\ndependency wiring"]
    Infra["Infrastructure adapters\nasyncpg repository\nPBKDF2 password hasher\nHMAC activation code hasher\nrandom code generator\nconsole email sender\nUTC clock"]
    Postgres["PostgreSQL\nusers\nschema_migrations"]
    Migrations["Versioned SQL migrations\nexecuted at startup"]
    Tests["Test suite\nunit, functional,\nintegration, regression"]

    Client --> FastAPI
    FastAPI --> UseCases
    UseCases --> Domain
    UseCases --> Ports
    Bootstrap --> FastAPI
    Bootstrap --> Infra
    Infra -. implements .-> Ports
    Infra --> Postgres
    Migrations --> Postgres
    Bootstrap --> Migrations
    Tests --> FastAPI
    Tests --> UseCases
    Tests --> Infra
```

## Dependency Direction

Runtime dependencies point inward:

```txt
presentation -> application -> domain
infrastructure -> application ports
bootstrap -> all layers for wiring only
```

The domain layer does not import FastAPI, asyncpg, Pydantic settings, or
infrastructure code. Application use cases depend on protocols, not concrete
database, security, or email implementations. Infrastructure classes implement
those protocols.

## Layers

### Domain

Location: `src/domain`

Responsibilities:

- Represent the `User` aggregate and account status.
- Validate email and activation code value objects.
- Enforce activation invariants, including timezone-aware UTC timestamps.
- Keep business rules independent from transport, database, and configuration.

### Application

Location: `src/application`

Responsibilities:

- Expose use cases for registration and activation.
- Define command objects and output DTOs.
- Define ports for persistence, email, hashing, code generation, and time.
- Translate domain and workflow failures into explicit application exceptions.

### Presentation

Location: `src/presentation`

Responsibilities:

- Define FastAPI routes.
- Validate HTTP request bodies with Pydantic schemas.
- Return response schemas.
- Use FastAPI `Depends` for dependency injection.
- Register exception handlers for stable HTTP error responses.

Routes intentionally stay thin: they map HTTP input to application commands,
call a use case, then map DTOs to HTTP responses.

### Infrastructure

Location: `src/infrastructure`

Responsibilities:

- Manage the asyncpg PostgreSQL pool.
- Execute raw SQL queries against PostgreSQL.
- Run versioned SQL migrations without Alembic.
- Hash passwords with PBKDF2-HMAC-SHA256.
- Generate numeric activation codes.
- Hash activation codes with HMAC-SHA256 before persistence.
- Send activation emails through a replaceable email adapter. The assessment
  implementation prints the code to the console, which keeps the third-party
  boundary explicit without requiring an external provider.

### Bootstrap

Location: `src/bootstrap`

Responsibilities:

- Create the FastAPI application.
- Register routers and exception handlers.
- Create long-lived infrastructure adapters during lifespan startup.
- Run SQL migrations before serving requests.
- Close the PostgreSQL pool during shutdown and on startup failure.
- Expose request dependencies that reuse startup state.

## Main Runtime Flows

### Registration

```mermaid
sequenceDiagram
    participant C as Client
    participant R as POST /users
    participant U as RegisterUserUseCase
    participant D as User domain
    participant DB as UserRepository
    participant E as EmailSender

    C->>R: email, password
    R->>U: RegisterUserCommand
    U->>DB: check existing email
    U->>D: create pending user
    U->>DB: save user
    U->>E: send activation code
    U-->>R: RegisteredUserDTO
    R-->>C: 201 Created
```

The database has a unique constraint on email. The repository translates unique
constraint violations into an application error so concurrent duplicate
registrations remain predictable.

### Activation

```mermaid
sequenceDiagram
    participant C as Client
    participant R as POST /users/activate
    participant U as ActivateUserUseCase
    participant DB as UserRepository
    participant D as User domain

    C->>R: Basic Auth + activation code
    R->>U: ActivateUserCommand
    U->>DB: load user by email
    U->>U: verify password, including dummy verification for unknown emails
    U->>U: verify activation code
    U->>D: check expiry and activate
    U->>DB: update user
    U-->>R: ActivatedUserDTO
    R-->>C: 200 OK
```

Activation codes expire after one minute. Date comparisons require timezone-aware
UTC datetimes so local or naive datetime mistakes fail fast.

## Database

The service uses PostgreSQL only. SQLite is not used anywhere.

The application schema is created by versioned SQL files in
`src/infrastructure/database/migrations`. Startup executes migrations in
filename order and records applied versions in `schema_migrations`.

Migration execution is serialized with a PostgreSQL advisory lock, which protects
startup migrations when several application instances start against the same
database.

## Tests

The test suite is labelled with pytest markers:

- `unit` covers application use cases with in-memory doubles.
- `functional` covers FastAPI routes and HTTP error mapping.
- `integration` covers asyncpg repositories and PostgreSQL persistence.
- `regression` protects previously fixed edge cases.

Docker Compose provides a dedicated `test` service and an isolated
`user_registration_test` database. Integration tests truncate their tables before
and after each run, so the application database is not modified by tests.
