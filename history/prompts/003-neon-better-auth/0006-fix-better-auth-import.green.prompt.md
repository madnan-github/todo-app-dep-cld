---
id: 0006
title: fix invalid better auth client import
stage: green
date: 2025-12-31
surface: agent
model: claude-opus-4-5-20251101
feature: 003-neon-better-auth
branch: 003-neon-better-auth
user: anonymous
command: start 1234
labels: ["better-auth", "frontend", "bug-fix"]
links:
  spec: specs/003-neon-better-auth/spec.md
files:
  - frontend/lib/auth.ts
tests:
  - next dev build verification
---

## Prompt

on frontend have this error: Build Error
Export emailPasswordClient doesn't exist in target module
./lib/auth.ts (2:1)

## Response snapshot

Corrected frontend/lib/auth.ts by removing the non-existent `emailPasswordClient` import. In Better Auth 1.x, the basic email/password functionality is built into the core `createAuthClient()` and does not require a separate client-side plugin import for standard flows. Verified that the frontend now compiles and runs successfully.

## Outcome

- ✅ Impact: Fixed frontend build error preventing application from starting.
- 🧪 Tests: Confirmed successful compile and 200 OK responses in `next dev` logs.
- 📁 Files: Updated `frontend/lib/auth.ts`.
- 🔁 Next prompts: None.

## Evaluation notes (flywheel)

- Failure modes observed: Incorrect assumption about client-side plugin requirements for Better Auth.
- Graders run and results (PASS/FAIL): PASS.
