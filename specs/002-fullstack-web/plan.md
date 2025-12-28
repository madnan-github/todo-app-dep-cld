# Implementation Plan: Full-Stack Web Todo Application

**Branch**: `002-fullstack-web` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web/spec.md`

**Note**: This plan transforms the Phase I console application into a multi-user web application with persistent storage, authentication, and advanced features (priorities, tags, search, filter, sort).

## Summary

Transform the Phase I console todo application into a modern, production-ready web application with:
- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS, React Server Components
- **Backend**: FastAPI (Python) with async/await, SQLModel ORM, JWT authentication
- **Database**: Neon PostgreSQL (serverless) with proper indexes for filtering/sorting
- **Authentication**: Better Auth with JWT tokens, 7-day sessions, user isolation
- **Features**: All Basic Level (CRUD) + Intermediate Level (priorities, tags, search, filter, sort)
- **Deployment**: Vercel (frontend), Railway/Render (backend), all free-tier services

The monorepo structure keeps frontend and backend in a single repository for simplified development and Claude Code context management.

## Technical Context

**Frontend**:
- **Language/Version**: TypeScript 5.x with Next.js 16+ (App Router)
- **Primary Dependencies**: Next.js, React 19, Tailwind CSS, Better Auth
- **Testing**: Jest + React Testing Library for components, Playwright for E2E
- **Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 years)

**Backend**:
- **Language/Version**: Python 3.13+
- **Primary Dependencies**: FastAPI, SQLModel, python-jose (JWT), passlib (password hashing)
- **Storage**: Neon PostgreSQL (serverless) via psycopg2/asyncpg
- **Testing**: pytest with httpx for async API tests
- **Target Platform**: Linux server (Docker container)

**Project Type**: Web application (monorepo with frontend/ and backend/ directories)

**Performance Goals**:
- API response time: <200ms p95 for CRUD operations
- UI render time: <2 seconds for task list load (up to 500 tasks)
- Search/filter operations: <1 second for results
- Support 10+ concurrent users without degradation

**Constraints**:
- Free-tier services only (Neon: 0.5GB storage, 190 compute hrs/mo; Vercel: 100GB bandwidth)
- Stateless backend (no server-side sessions, JWT only)
- No paid APIs or services
- Database queries must use proper indexes to stay within free tier compute limits

**Scale/Scope**:
- Initial target: 50 users, ~10,000 total tasks across all users
- Per-user limit: 500 tasks (tested performance threshold)
- 47 functional requirements across 7 categories
- 10 prioritized user stories (P1-P4)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **I. Spec-Driven Development** | Specification exists before implementation | ✅ PASS | spec.md complete with 47 requirements, 10 user stories |
| **II. AI-First Development** | Use Claude Code for implementation | ✅ PASS | Using specialized agents (nextjs-frontend-agent, fastapi-backend-agent, authentication-agent) |
| **III. Test-First (TDD)** | Tests before implementation code | ⚠️ DEFER | Will be enforced during /sp.tasks phase; tests defined in acceptance criteria |
| **IV. Free-Tier First** | All services use free tiers | ✅ PASS | Neon (0.5GB), Vercel (100GB), Railway/Render free tier, Better Auth (self-hosted) |
| **V. Progressive Architecture** | Builds on Phase I without breaking it | ✅ PASS | Phase I console app remains functional; Phase II adds web interface |
| **VI. Stateless & Cloud-Native** | Stateless backend, horizontally scalable | ✅ PASS | JWT auth, no server sessions, database is source of truth |
| **VII. Simplicity & YAGNI** | Implement only what's specified | ✅ PASS | No features beyond spec; using standard libraries where possible |

**Gate Result**: ✅ **PASSED** - Proceed to Phase 0 research.

**Notes**:
- TDD will be strictly enforced during task execution phase (/sp.tasks)
- All technology choices align with constitution Phase II stack requirements
- Monorepo structure enables Claude Code to work on both frontend and backend in single context

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── api-spec.yaml    # OpenAPI 3.0 specification
│   └── database-schema.sql  # PostgreSQL schema DDL
├── checklists/          # Quality validation
│   └── requirements.md  # Specification quality checklist (COMPLETE)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Monorepo structure (web application with shared context)
todo-app-web/
├── .specify/            # Spec-Kit configuration
│   ├── memory/
│   │   └── constitution.md
│   ├── scripts/
│   └── templates/
├── specs/               # Feature specifications
│   ├── 001-console-todo-crud/  # Phase I (COMPLETE)
│   └── 002-fullstack-web/      # Phase II (CURRENT)
├── history/             # Prompt History Records
│   └── prompts/
│       ├── 001-console-todo-crud/
│       └── 002-fullstack-web/
├── CLAUDE.md            # Root AI instructions
├── README.md            # Project documentation
├── docker-compose.yml   # Local development setup
│
├── frontend/            # Next.js 16+ application
│   ├── app/             # App Router pages
│   │   ├── layout.tsx
│   │   ├── page.tsx     # Landing page
│   │   ├── (auth)/      # Auth routes (route group)
│   │   │   ├── signin/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   ├── dashboard/   # Protected dashboard
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── api/         # API routes for Better Auth
│   │       └── auth/
│   │           └── [...better-auth]/
│   │               └── route.ts
│   ├── components/      # React components
│   │   ├── ui/          # Reusable UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── badge.tsx
│   │   │   └── card.tsx
│   │   ├── tasks/       # Task-specific components
│   │   │   ├── task-list.tsx
│   │   │   ├── task-item.tsx
│   │   │   ├── task-form.tsx
│   │   │   ├── task-filter.tsx
│   │   │   ├── task-sort.tsx
│   │   │   └── tag-input.tsx
│   │   └── auth/        # Auth components
│   │       ├── signin-form.tsx
│   │       └── signup-form.tsx
│   ├── lib/             # Utilities and configurations
│   │   ├── api.ts       # API client with JWT injection
│   │   ├── auth.ts      # Better Auth configuration
│   │   └── utils.ts     # Helper functions (cn, etc.)
│   ├── types/           # TypeScript type definitions
│   │   └── index.ts     # Task, Tag, User, API types
│   ├── __tests__/       # Component tests
│   │   ├── components/
│   │   └── integration/
│   ├── public/          # Static assets
│   ├── CLAUDE.md        # Frontend-specific AI instructions
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── .env.local.example
│
└── backend/             # FastAPI application
    ├── src/
    │   ├── models.py    # SQLModel database models
    │   ├── schemas.py   # Pydantic request/response schemas
    │   ├── database.py  # Neon PostgreSQL connection
    │   ├── auth.py      # JWT verification middleware
    │   ├── config.py    # Environment configuration
    │   ├── main.py      # FastAPI app entry point
    │   └── routes/      # API route handlers
    │       ├── __init__.py
    │       ├── auth.py  # Better Auth integration
    │       ├── tasks.py # Task CRUD + filter/sort
    │       └── tags.py  # Tag management
    ├── tests/           # Backend tests
    │   ├── __init__.py
    │   ├── test_auth.py
    │   ├── test_tasks.py
    │   ├── test_tags.py
    │   └── test_isolation.py
    ├── alembic/         # Database migrations (optional)
    ├── CLAUDE.md        # Backend-specific AI instructions
    ├── pyproject.toml   # UV package management
    ├── requirements.txt # Pinned dependencies
    └── .env.example
```

**Structure Decision**: Monorepo with `frontend/` and `backend/` directories selected because:
1. Single repository simplifies Claude Code context management (sees both codebases)
2. Shared type definitions can be referenced across frontend/backend
3. Single PR workflow for features that span both layers
4. Simplified deployment coordination
5. Better spec-kit integration (single `.specify/` directory)

Alternative rejected: Separate repositories would require multi-workspace Claude Code setup and complicate cross-cutting changes.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution principles are satisfied:
- Spec-driven: Complete specification with 47 requirements
- AI-first: Using specialized agents for implementation
- Free-tier: All services within free tier limits
- Stateless: JWT-based auth, no server sessions
- YAGNI: Only implementing specified features
