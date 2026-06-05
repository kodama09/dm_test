# Changelog

## 0.2.0 - Configuration and runtime bootstrap

MR: [#2 - Configuration and runtime bootstrap](https://github.com/kodama09/dm_test/pull/2)

### ✨ Add

• Add cached application settings loaded with pydantic-settings.
• Add Docker Compose runtime with PostgreSQL and healthcheck.
• Add an application Dockerfile for the FastAPI service.
• Add setuptools packaging configuration for container builds.
• Add changelog structure and the feature finalization decision.

### 🧹 Remove

• None.

### 🩹 Fix

• None.

### 🧪 Test

• Validate settings loading and environment override locally.
• Validate Docker Compose YAML syntax.
• Validate the health endpoint still returns application metadata.

### 🔒 Security

• Keep local environment values out of version control through `.env`.
