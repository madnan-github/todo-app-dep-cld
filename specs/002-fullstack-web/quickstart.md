# Quickstart Guide: Phase II Full-Stack Web Application

**Feature**: 002-fullstack-web
**Date**: 2025-12-28
**Estimated Setup Time**: 30-45 minutes

This guide walks you through setting up the full-stack development environment for Phase II.

---

## Prerequisites

Before you begin, ensure you have:

| Requirement | Minimum Version | Installation |
|-------------|----------------|--------------|
| Node.js | 20.x | [nodejs.org](https://nodejs.org/) |
| Python | 3.13+ | [python.org](https://www.python.org/) |
| UV | Latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Git | 2.x | [git-scm.com](https://git-scm.com/) |
| PostgreSQL CLI (psql) | 15+ | For database inspection (optional) |

---

## Step 1: Clone and Navigate to Repository

```bash
# If not already cloned
git clone <your-repository-url>
cd todo-app-web

# Checkout the Phase II branch
git checkout 002-fullstack-web
```

---

## Step 2: Set Up Database (Neon PostgreSQL)

### 2.1 Create Neon Account

1. Go to [neon.tech](https://neon.tech)
2. Sign up with GitHub (free tier: 0.5GB storage, 190 compute hours/month)
3. Create a new project: **TaskFlow**
4. Note your connection string (it looks like `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb`)

### 2.2 Initialize Database Schema

```bash
# Connect to your Neon database
psql "postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb"

# Run the schema creation script
\i specs/002-fullstack-web/contracts/database-schema.sql

# Verify tables were created
\dt

# Expected output:
#  Schema |    Name    | Type  |  Owner
# --------+------------+-------+---------
#  public | users      | table | postgres
#  public | tasks      | table | postgres
#  public | tags       | table | postgres
#  public | task_tags  | table | postgres

# Exit psql
\q
```

---

## Step 3: Set Up Backend (FastAPI)

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Environment File

```bash
cp .env.example .env
```

Edit `.env` file with your values:

```env
# Neon PostgreSQL connection string
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb

# Shared secret for JWT signing (use same value in frontend)
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
BETTER_AUTH_SECRET=your-secret-key-here-use-python-command-above

# CORS allowed origins (frontend URL)
CORS_ORIGINS=http://localhost:3000

# API settings
API_HOST=0.0.0.0
API_PORT=8000
```

### 3.3 Install Dependencies

```bash
# Install dependencies using UV
uv sync

# This creates a virtual environment and installs:
# - fastapi
# - uvicorn[standard]
# - sqlmodel
# - python-jose[cryptography]
# - passlib[bcrypt]
# - python-multipart
# - httpx (for tests)
# - pytest (for tests)
```

### 3.4 Run Database Migrations (Optional)

If using Alembic for migrations:

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 3.5 Start Backend Server

```bash
# Development mode (auto-reload on code changes)
uvicorn src.main:app --reload --port 8000

# Server should start at: http://localhost:8000
# API docs available at: http://localhost:8000/docs (Swagger UI)
# Alternative docs at: http://localhost:8000/redoc (ReDoc)
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 4: Set Up Frontend (Next.js)

### 4.1 Navigate to Frontend Directory

Open a **new terminal** (keep backend running) and navigate:

```bash
cd frontend
```

### 4.2 Create Environment File

```bash
cp .env.local.example .env.local
```

Edit `.env.local` file with your values:

```env
# Shared secret for JWT signing (SAME as backend)
BETTER_AUTH_SECRET=your-secret-key-here-same-as-backend

# Neon PostgreSQL connection string (Better Auth needs direct DB access)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb

# Backend API URL (public, accessible from browser)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4.3 Install Dependencies

```bash
# Install Node dependencies
npm install

# This installs:
# - next@16
# - react@19
# - react-dom@19
# - typescript
# - tailwindcss
# - better-auth
# - and other dependencies
```

### 4.4 Start Frontend Development Server

```bash
# Development mode (fast refresh on code changes)
npm run dev

# Server should start at: http://localhost:3000
```

**Expected output:**
```
   ▲ Next.js 16.0.0
   - Local:        http://localhost:3000
   - Network:      http://192.168.1.x:3000

 ✓ Ready in 2.5s
```

---

## Step 5: Verify Installation

### 5.1 Open Application in Browser

Navigate to: [http://localhost:3000](http://localhost:3000)

You should see the landing page with **Sign Up** and **Sign In** buttons.

### 5.2 Test API Endpoints

Visit the auto-generated API documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 5.3 Create Test Account

1. Click **Sign Up** on the frontend
2. Enter:
   - Email: `test@example.com`
   - Password: `password123`
3. You should be redirected to the dashboard

### 5.4 Create Test Task

1. On the dashboard, enter a task:
   - Title: "Test task"
   - Priority: High
   - Tags: "test"
2. Click **Add Task**
3. Task should appear in the list with a red "HIGH" badge

### 5.5 Verify Database

```bash
# Connect to database
psql "postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb"

# Check user was created
SELECT id, email, name, created_at FROM users;

# Check task was created
SELECT id, title, priority, completed FROM tasks;

# Check tag was created
SELECT id, name FROM tags;

# Exit
\q
```

---

## Step 6: Run Tests

### 6.1 Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Expected output:
# tests/test_auth.py ............     [  40%]
# tests/test_tasks.py ............    [  80%]
# tests/test_isolation.py .....      [ 100%]
#
# =================== 25 passed in 3.42s ===================
```

### 6.2 Frontend Tests

```bash
cd frontend

# Run component tests
npm test

# Run E2E tests (requires app running)
npx playwright test

# Expected output:
# PASS  components/tasks/task-form.test.tsx
# PASS  components/tasks/task-list.test.tsx
# PASS  lib/api.test.ts
#
# Tests: 15 passed, 15 total
```

---

## Step 7: Development Workflow

### 7.1 Typical Day-to-Day Commands

**Backend:**
```bash
cd backend
uvicorn src.main:app --reload  # Start API server
pytest -v                       # Run tests
alembic upgrade head            # Apply migrations
```

**Frontend:**
```bash
cd frontend
npm run dev                     # Start dev server
npm test                        # Run tests
npm run build                   # Build for production
```

### 7.2 Docker Compose (Alternative)

For running both frontend and backend together:

```bash
# From repository root
docker-compose up

# This starts:
# - Backend at http://localhost:8000
# - Frontend at http://localhost:3000
# - PostgreSQL at localhost:5432 (if using local instead of Neon)
```

---

## Step 8: Next Steps

After completing this quickstart, proceed to:

1. **Review Specifications**: Read `specs/002-fullstack-web/spec.md` for detailed requirements
2. **Understand Architecture**: Review `specs/002-fullstack-web/plan.md` for system design
3. **API Reference**: Bookmark `http://localhost:8000/docs` for API exploration
4. **Start Implementing**: Follow `/sp.tasks` to generate implementation tasks

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Ensure you're in the virtual environment:
```bash
cd backend
source .venv/bin/activate  # or: .venv\Scripts\activate on Windows
uv sync
```

### Frontend won't start

**Error**: `Error: ENOENT: no such file or directory, open 'node_modules'`

**Solution**: Install dependencies:
```bash
cd frontend
npm install
```

### Database connection fails

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**: Check your `DATABASE_URL` in `.env` files:
1. Verify connection string is correct (copy from Neon dashboard)
2. Ensure database is not paused (Neon auto-pauses after inactivity)
3. Test connection with `psql` first

### JWT token errors

**Error**: `401 Unauthorized` or `Invalid token`

**Solution**: Ensure `BETTER_AUTH_SECRET` is **identical** in:
- `backend/.env`
- `frontend/.env.local`

Regenerate secret if needed:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Port already in use

**Error**: `EADDRINUSE: address already in use :::3000`

**Solution**: Kill process using the port:
```bash
# Find process ID
lsof -ti:3000  # or: lsof -ti:8000 for backend

# Kill process
kill -9 <PID>
```

### CORS errors in browser console

**Error**: `Access to fetch at 'http://localhost:8000' has been blocked by CORS policy`

**Solution**: Check `backend/src/main.py` CORS middleware:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must match frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Environment Variables Reference

### Backend (backend/.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | JWT signing secret (32+ chars) | `abc123...` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:3000` |
| `API_HOST` | Bind address | `0.0.0.0` |
| `API_PORT` | Port to listen on | `8000` |

### Frontend (frontend/.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `BETTER_AUTH_SECRET` | JWT signing secret (SAME as backend) | `abc123...` |
| `DATABASE_URL` | PostgreSQL connection string (for Better Auth) | `postgresql://user:pass@host/db` |
| `NEXT_PUBLIC_API_URL` | Backend API URL (browser-accessible) | `http://localhost:8000` |

---

## Additional Resources

- **OpenAPI Spec**: `specs/002-fullstack-web/contracts/api-spec.yaml`
- **Database Schema**: `specs/002-fullstack-web/contracts/database-schema.sql`
- **Data Model**: `specs/002-fullstack-web/data-model.md`
- **Research Decisions**: `specs/002-fullstack-web/research.md`
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **Better Auth Docs**: [better-auth.com](https://better-auth.com/)
- **Neon Docs**: [neon.tech/docs](https://neon.tech/docs)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the specification in `specs/002-fullstack-web/spec.md`
3. Consult the API documentation at `http://localhost:8000/docs`
4. Check environment variables are set correctly

**Ready to build!** 🚀 Proceed to `/sp.tasks` to generate implementation tasks.
