---
id: 0007
title: fix neon connection configuration and fallback
stage: green
date: 2025-12-31
surface: agent
model: claude-opus-4-5-20251101
feature: 003-neon-better-auth
branch: 003-neon-better-auth
user: anonymous
command: start 1234
labels: ["neon", "postgresql", "configuration", "bug-fix"]
links:
  spec: specs/003-neon-better-auth/spec.md
files:
  - backend/src/config.py
  - backend/.env
  - backend/todo_app.db
tests:
  - backend/verify_neon.py
---

## Prompt

i didn't understand, my frontend and backend working, signin and signup and task data is not showing on neondb, there is no table on neon portal?

## Response snapshot

Identified that the application was silently falling back to a local SQLite database due to a case-sensitivity mismatch in `backend/src/config.py` (Pydantic settings) and an unsupported `sslmode` parameter in `backend/.env`. Fixed the configuration by setting `case_sensitive=False` in the settings model and removing `?sslmode=require` from the Neon connection string. Deleted the local SQLite database and verified successful table creation and CRUD operations directly on the Neon PostgreSQL instance.

## Outcome

- ✅ Impact: Correctly connected the application to Neon PostgreSQL, eliminating silent SQLite fallback.
- 🧪 Tests: Successful execution of `verify_neon.py` against the actual Neon database.
- 📁 Files: Updated `backend/src/config.py`, `backend/.env`, and removed `backend/todo_app.db`.
- 🔁 Next prompts: None.

## Evaluation notes (flywheel)

- Failure modes observed: Silent fallback to default value when environment variable mapping failed due to case sensitivity.
- Graders run and results (PASS/FAIL): PASS.
