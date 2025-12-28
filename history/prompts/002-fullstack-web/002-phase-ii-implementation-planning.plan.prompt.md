---
id: 002
title: Phase II Implementation Planning
stage: plan
date: 2025-12-28
surface: agent
model: claude-opus-4-5-20251101
feature: 002-fullstack-web
branch: 002-fullstack-web
user: ruser
command: /sp.plan
labels: ["phase-ii", "architecture", "technical-design", "data-model", "api-contracts"]
links:
  spec: specs/002-fullstack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-web/plan.md
  - specs/002-fullstack-web/research.md
  - specs/002-fullstack-web/data-model.md
  - specs/002-fullstack-web/quickstart.md
  - specs/002-fullstack-web/contracts/api-spec.yaml
  - specs/002-fullstack-web/contracts/database-schema.sql
  - CLAUDE.md (updated with new technology context)
tests:
  - Constitution check passed (7/7 principles)
  - Data model validation (4 entities, 10 indexes, 14 constraints)
  - API contract validation (8 endpoints covering 47 requirements)
---

## Prompt

User requested: "Phase II" (triggering /sp.plan command)

Context: User completed Phase I (console app with 179 passing tests) and created comprehensive Phase II specification (10 user stories, 47 functional requirements). User wants to proceed with implementation planning for the full-stack web application.

The specification defines:
- Transformation of Phase I console app to multi-user web application
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS, Better Auth
- Backend: FastAPI with async/await, SQLModel ORM, JWT verification
- Database: Neon PostgreSQL with proper indexes
- Features: All Basic Level (CRUD) + Intermediate Level (priorities, tags, search, filter, sort)
- Security: User isolation via JWT, input validation, XSS/SQL injection prevention
- Deployment: Vercel (frontend), Railway/Render (backend), all free-tier services

## Response snapshot

Created complete implementation plan with Phase 0 (Research) and Phase 1 (Design) artifacts:

**Phase 0: Research & Technical Decisions** (`research.md`):
1. Frontend Framework: Next.js 16+ App Router (React Server Components, streaming, TypeScript)
2. Authentication: Better Auth + JWT (self-hosted, 7-day sessions, stateless)
3. Backend API: FastAPI async (high performance, type safety, auto docs)
4. ORM: SQLModel (Pydantic integration, type safety, less boilerplate)
5. Database: Neon PostgreSQL (serverless, free tier, full SQL support)
6. Styling: Tailwind CSS only (utility-first, responsive, consistent)
7. API Security: JWT verification middleware (stateless auth, user isolation)
8. Search & Filter: Database-level with query parameters (performance, indexed)
9. Tag Autocomplete: Database LIKE queries (simple, fast with index)
10. Deployment: Vercel + Railway/Render (free tiers, production-ready)

Each decision includes:
- Rationale with specific benefits
- Alternatives considered with rejection reasons
- Implementation patterns with code examples

**Phase 1: Data Model** (`data-model.md`):
- **4 Entities**: User (Better Auth), Task, Tag, TaskTag (junction)
- **Field Specifications**: All fields with types, constraints, defaults
- **Relationships**: 1:N (User→Tasks, User→Tags), M:N (Tasks↔Tags)
- **10 Indexes**: Covering user isolation, filtering, sorting, tag autocomplete
- **14 Constraints**: Uniqueness, foreign keys, NOT NULL, CHECK, enum
- **Query Patterns**: 5 common query patterns with SQL examples
- **Performance Analysis**: Expected query times (<50ms to <200ms)
- **Migration Strategy**: Phase I → Phase II (no data migration needed)

**Phase 1: API Contracts** (`contracts/api-spec.yaml`):
- **OpenAPI 3.0 specification** with 8 endpoints:
  - `/api/auth/signup` (POST) - Create account
  - `/api/auth/signin` (POST) - Authenticate user
  - `/api/{user_id}/tasks` (GET) - List tasks with filters/sort
  - `/api/{user_id}/tasks` (POST) - Create task
  - `/api/{user_id}/tasks/{task_id}` (GET) - Get task details
  - `/api/{user_id}/tasks/{task_id}` (PUT) - Update task
  - `/api/{user_id}/tasks/{task_id}` (DELETE) - Delete task
  - `/api/{user_id}/tasks/{task_id}/complete` (PATCH) - Toggle completion
  - `/api/{user_id}/tags/autocomplete` (GET) - Tag suggestions
- **Request/Response Schemas**: Task, TaskCreate, TaskUpdate, Tag, User, Error
- **Security Scheme**: JWT Bearer token authentication
- **Error Responses**: 400, 401, 403, 404 with clear descriptions

**Phase 1: Database Schema** (`contracts/database-schema.sql`):
- Complete DDL for all 4 tables with constraints and indexes
- Enum type for task priority
- Auto-update trigger for `updated_at` timestamp
- Sample data (commented out) for testing
- Verification queries for schema validation

**Phase 1: Quickstart Guide** (`quickstart.md`):
- Step-by-step setup instructions (8 steps)
- Prerequisites with installation links
- Environment variable configuration
- Database initialization with Neon
- Backend and frontend startup commands
- Verification steps and troubleshooting
- Estimated setup time: 30-45 minutes

**Technical Context** (in `plan.md`):
- Frontend: TypeScript 5.x + Next.js 16+ (App Router)
- Backend: Python 3.13+ + FastAPI
- Performance goals: <200ms API, <2s UI load, <1s filter/search
- Scale targets: 50 users, 10k total tasks, 500 tasks per user
- Constraints: Free-tier limits, stateless backend, indexed queries

**Constitution Check** (in `plan.md`):
✅ All 7 principles passed:
- Spec-driven (47 requirements), AI-first (using specialized agents), TDD (deferred to tasks phase), Free-tier (Neon/Vercel/Railway free), Progressive (builds on Phase I), Stateless (JWT auth), YAGNI (spec-only features)

**Project Structure** (in `plan.md`):
- Monorepo with `frontend/` and `backend/` directories
- Complete directory tree with all files and components
- Structure decision documented with rationale

## Outcome

- ✅ Impact: Created production-ready implementation plan with complete technical design, data model, API contracts, and developer quickstart guide
- 🧪 Tests: Constitution check 7/7 PASS, Data model validates all 47 requirements, API spec covers all user stories
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, api-spec.yaml, database-schema.sql (6 planning artifacts)
- 🔁 Next prompts: `/sp.tasks` to generate actionable task breakdown with TDD test cases
- 🧠 Reflection: Plan successfully bridges specification (WHAT) to implementation (HOW) with clear technical decisions, monorepo structure enables Claude Code to work on both frontend and backend in single context, all technology choices align with constitution and free-tier requirements

## Evaluation notes (flywheel)

- Failure modes observed: None - all constitution gates passed, no technical blockers identified
- Graders run and results (PASS/FAIL): Constitution check PASS (7/7), Data model completeness PASS (4 entities, all relationships defined), API coverage PASS (8 endpoints map to 47 requirements), Free-tier compliance PASS (all services documented with limits)
- Prompt variant (if applicable): N/A - standard planning workflow
- Next experiment (smallest change to try): N/A - plan complete and ready for task generation
