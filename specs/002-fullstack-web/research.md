# Research: Full-Stack Web Todo Application

**Feature**: 002-fullstack-web
**Date**: 2025-12-28
**Purpose**: Document technical decisions and patterns for Phase II implementation

---

## 1. Frontend Framework: Next.js 16+ with App Router

### Decision
Use Next.js 16+ with **App Router** (not Pages Router) for the frontend framework.

### Rationale
- **React Server Components (RSC)**: Enables data fetching on server, reducing client bundle size
- **Streaming**: Improves perceived performance with progressive rendering
- **Built-in routing**: File-system based routing with layouts and route groups
- **TypeScript support**: First-class TypeScript integration
- **Vercel deployment**: Seamless deployment to Vercel free tier
- **Constitution alignment**: Specified in Phase II technology stack

### Alternatives Considered
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Create React App (CRA) | Simple setup | No SSR, deprecated | No server-side rendering, not maintained |
| Vite + React | Fast HMR | Manual routing, no RSC | Requires additional setup for SSR/routing |
| Pages Router | Stable, well-documented | Older pattern, no RSC | App Router is the future, better performance |

### Implementation Pattern
```typescript
// app/dashboard/page.tsx - Server Component (default)
export default async function DashboardPage() {
  // Can fetch data directly on server
  return <TaskList />
}

// components/tasks/task-form.tsx - Client Component (interactive)
'use client'
export function TaskForm() {
  const [title, setTitle] = useState('')
  // Interactive UI with state
}
```

---

## 2. Authentication: Better Auth with JWT

### Decision
Use **Better Auth** with JWT plugin for authentication, JWT tokens for API authorization.

### Rationale
- **Self-hosted**: No external auth service fees (free-tier requirement)
- **JWT support**: Native JWT token generation for backend API authentication
- **TypeScript-first**: Full type safety for auth flows
- **Database integration**: Works with Neon PostgreSQL
- **7-day sessions**: Configurable session duration (spec requirement)
- **Email/password**: Supports required authentication method

### Alternatives Considered
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| NextAuth.js | Popular, good docs | Session-based by default, heavier | Requires adapter for JWT, more complex |
| Auth0 | Enterprise features | Paid beyond free tier | Free tier limits (7000 users) might be restrictive |
| Supabase Auth | Integrated with Supabase DB | Vendor lock-in | Not using Supabase DB (using Neon) |
| Custom JWT | Full control | More implementation work | Better Auth provides this out-of-box |

### Implementation Pattern
```typescript
// lib/auth.ts - Better Auth configuration
import { BetterAuth } from 'better-auth'

export const auth = new BetterAuth({
  database: {
    provider: 'pg',
    url: process.env.DATABASE_URL,
  },
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET,
    expiresIn: '7d',
  },
  emailPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
})

// lib/api.ts - API client with JWT injection
class APIClient {
  private async getToken(): Promise<string> {
    const session = await auth.getSession()
    return session?.accessToken || ''
  }

  private async request<T>(url: string, options: RequestInit): Promise<T> {
    const token = await this.getToken()
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
      },
    })
    if (response.status === 401) {
      // Redirect to signin
      window.location.href = '/signin'
    }
    return response.json()
  }
}
```

---

## 3. Backend API: FastAPI with Async/Await

### Decision
Use **FastAPI** with async/await patterns for all API endpoints.

### Rationale
- **High performance**: Comparable to Node.js and Go for async operations
- **Type safety**: Pydantic models provide runtime validation
- **Auto documentation**: OpenAPI/Swagger generated automatically
- **Async database**: Works with asyncpg for non-blocking database queries
- **Python 3.13+**: Modern Python with latest async features
- **Constitution alignment**: Specified in Phase II technology stack

### Alternatives Considered
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Flask | Simpler, lightweight | Sync-only by default, manual typing | Not async, slower for I/O-bound tasks |
| Django + DRF | Full-featured ORM | Heavy, slower startup | Overkill for API-only backend |
| Node.js/Express | JavaScript ecosystem | Different language than Phase I | Want to continue with Python skillset |

### Implementation Pattern
```python
# src/main.py - FastAPI app
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# src/routes/tasks.py - Async endpoints
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[TaskResponse]:
    # Verify user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Async database query
    result = await session.execute(
        select(Task).where(Task.user_id == user_id)
    )
    tasks = result.scalars().all()
    return tasks
```

---

## 4. ORM: SQLModel with Async Support

### Decision
Use **SQLModel** with asyncpg driver for database operations.

### Rationale
- **Pydantic integration**: Database models are also Pydantic models
- **Type safety**: Full Python type hints, IDE autocomplete
- **SQLAlchemy foundation**: Mature ORM with async support
- **Less boilerplate**: Single model for database and API schemas
- **Migration support**: Compatible with Alembic for schema changes

### Alternatives Considered
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| SQLAlchemy Core | More control, explicit | More boilerplate, no Pydantic | SQLModel provides Pydantic integration |
| Tortoise ORM | Async-first | Less mature, smaller community | SQLModel more stable, better documented |
| Prisma | Great DX, type-safe | Primarily for Node.js | Python support experimental |

### Implementation Pattern
```python
# src/models.py - SQLModel models
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
```

---

## 5. Database: Neon PostgreSQL with Indexes

### Decision
Use **Neon PostgreSQL** (serverless) with proper indexes for filtering/sorting performance.

### Rationale
- **Serverless**: Auto-scaling, pay only for compute used (190 hrs/mo free)
- **PostgreSQL**: Full SQL support, ACID compliance, robust
- **Free tier**: 0.5GB storage sufficient for development and initial launch
- **Connection pooling**: Built-in connection pooling reduces overhead
- **Branching**: Database branching for testing (optional future use)

### Alternatives Considered
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Supabase Postgres | Integrated auth | Vendor lock-in with auth | Using Better Auth, not Supabase Auth |
| PlanetScale | MySQL-compatible, branching | MySQL not PostgreSQL | Preference for PostgreSQL (JSON, arrays) |
| Render PostgreSQL | Free tier | Only 90 days free | Neon free tier permanent |
| SQLite | Local, simple | Not scalable, no user isolation | Multi-user requires proper database |

### Index Strategy
```sql
-- Primary indexes for lookups
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Composite index for filtered sorting
CREATE INDEX idx_tasks_user_completed_priority ON tasks(user_id, completed, priority);

-- Tag indexes
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);
```

---

## 6. Styling: Tailwind CSS Only

### Decision
Use **Tailwind CSS** exclusively for styling (no custom CSS files, no CSS-in-JS).

### Rationale
- **Utility-first**: Rapid development with utility classes
- **Consistent spacing**: Tailwind's spacing scale prevents inconsistencies
- **Responsive design**: Built-in breakpoints (sm, md, lg, xl)
- **Small bundle**: Unused classes purged in production
- **No CSS conflicts**: No global styles, no cascade issues
- **Specification requirement**: Spec explicitly requires Tailwind only

### Alternatives Considered
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| CSS Modules | Scoped styles | Separate files, verbose | Spec requires Tailwind only |
| Styled Components | Dynamic styles in JS | Runtime cost, complexity | Adds unnecessary complexity |
| Emotion | CSS-in-JS, performant | Learning curve | Not in spec, unnecessary |

### Implementation Pattern
```tsx
// components/tasks/task-item.tsx - Tailwind utility classes
export function TaskItem({ task }: { task: Task }) {
  return (
    <div className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
      <div className="flex items-center gap-3">
        {/* Priority badge - colored based on priority */}
        <span className={cn(
          "px-2 py-1 rounded text-xs font-medium",
          task.priority === 'high' && "bg-red-100 text-red-800",
          task.priority === 'medium' && "bg-yellow-100 text-yellow-800",
          task.priority === 'low' && "bg-green-100 text-green-800"
        )}>
          {task.priority}
        </span>

        {/* Title with conditional strikethrough */}
        <h3 className={cn(
          "font-medium",
          task.completed && "line-through text-gray-500"
        )}>
          {task.title}
        </h3>
      </div>

      {/* Tags as pills */}
      <div className="flex gap-2">
        {task.tags.map(tag => (
          <span key={tag.id} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
            {tag.name}
          </span>
        ))}
      </div>
    </div>
  )
}
```

---

## 7. API Security: JWT Verification Middleware

### Decision
Implement JWT verification middleware in FastAPI that validates tokens on every protected endpoint.

### Rationale
- **Stateless authentication**: No server-side sessions to manage
- **User isolation**: Token contains user_id, verified on every request
- **Security best practice**: Never trust user_id from request body
- **Horizontal scalability**: Any backend instance can verify tokens
- **Specification requirement**: FR-037, FR-038 mandate JWT verification

### Implementation Pattern
```python
# src/auth.py - JWT verification middleware
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from typing import Optional

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> User:
    """Verify JWT token and return current user."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from database
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

# src/routes/tasks.py - Protected endpoint
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),  # JWT verification
) -> List[TaskResponse]:
    # Verify URL user_id matches token user_id
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # User identity verified, proceed with query
    tasks = await get_user_tasks(user_id)
    return tasks
```

---

## 8. Search & Filter: Query Parameters with Database Indexes

### Decision
Implement search and filtering using **query parameters** with database-level filtering (not client-side).

### Rationale
- **Performance**: Filtering 500 tasks in database faster than transferring all to client
- **Free tier**: Reduces data transfer, stays within Neon compute limits
- **Indexes**: Proper indexes make filtered queries fast (<100ms)
- **Composable**: Multiple filters combine with AND logic in SQL WHERE clause
- **Specification requirement**: FR-026 through FR-035 define filter/search behavior

### Implementation Pattern
```python
# src/routes/tasks.py - Filtered query
from sqlalchemy import select, or_, and_

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    status: Optional[str] = Query(None, regex="^(all|pending|completed)$"),
    priority: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),  # Comma-separated
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("created_at", regex="^(created_at|priority|title)$"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    session: AsyncSession = Depends(get_session),
) -> List[TaskResponse]:
    # Start with base query
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Apply priority filter
    if priority:
        priorities = priority.split(",")
        query = query.where(Task.priority.in_(priorities))

    # Apply search filter (ILIKE for case-insensitive)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # Apply tag filter (requires JOIN)
    if tags:
        tag_names = tags.split(",")
        query = query.join(Task.tags).where(Tag.name.in_(tag_names))

    # Apply sorting
    sort_column = getattr(Task, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks
```

---

## 9. Tag Autocomplete: Database Query with LIKE

### Decision
Implement tag autocomplete using **database query** that searches existing user tags.

### Rationale
- **Real-time**: Query database as user types (debounced)
- **User-specific**: Only shows tags from current user's tasks
- **Simple**: No need for dedicated search index for small tag counts
- **Fast**: Index on `tags.name` makes LIKE queries fast for prefix matching

### Implementation Pattern
```python
# src/routes/tags.py - Tag autocomplete endpoint
@router.get("/api/{user_id}/tags/autocomplete")
async def autocomplete_tags(
    user_id: str,
    q: str = Query(..., min_length=1),  # Search query
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[str]:
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Find tags matching prefix for this user's tasks
    query = (
        select(Tag.name)
        .join(TaskTag)
        .join(Task)
        .where(Task.user_id == user_id)
        .where(Tag.name.ilike(f"{q}%"))  # Prefix matching
        .distinct()
        .limit(10)  # Max 10 suggestions
    )

    result = await session.execute(query)
    tag_names = result.scalars().all()
    return tag_names
```

```typescript
// components/tasks/tag-input.tsx - Frontend autocomplete
'use client'
import { useState, useEffect } from 'react'
import { useDe bounce } from '@/lib/hooks'

export function TagInput({ userId, value, onChange }: TagInputProps) {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState<string[]>([])
  const debouncedQuery = useDebounce(query, 300)  // 300ms delay

  useEffect(() => {
    if (debouncedQuery.length >= 1) {
      fetch(`/api/${userId}/tags/autocomplete?q=${debouncedQuery}`)
        .then(res => res.json())
        .then(setSuggestions)
    } else {
      setSuggestions([])
    }
  }, [debouncedQuery, userId])

  return (
    <div className="relative">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Add tags..."
        className="w-full px-3 py-2 border rounded"
      />
      {suggestions.length > 0 && (
        <ul className="absolute z-10 w-full bg-white border rounded-b shadow-lg">
          {suggestions.map(tag => (
            <li
              key={tag}
              onClick={() => {
                onChange([...value, tag])
                setQuery('')
                setSuggestions([])
              }}
              className="px-3 py-2 hover:bg-gray-100 cursor-pointer"
            >
              {tag}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
```

---

## 10. Deployment: Vercel + Railway/Render

### Decision
Deploy frontend to **Vercel** and backend to **Railway** or **Render** free tiers.

### Rationale
- **Vercel**: Best Next.js hosting, 100GB bandwidth free tier, automatic HTTPS
- **Railway**: 500 hours free compute ($5 credit), Docker support, simple deployment
- **Render**: Alternative to Railway, similar free tier, good for Python/FastAPI
- **Constitution requirement**: Free-tier first principle, all deployments must be free

### Deployment Configuration

**Frontend (Vercel)**:
```bash
# vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "BETTER_AUTH_SECRET": "@better-auth-secret",
    "DATABASE_URL": "@database-url",
    "NEXT_PUBLIC_API_URL": "https://api.yourdomain.com"
  }
}
```

**Backend (Railway/Render)**:
```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Railway Deploy**:
1. Connect GitHub repository
2. Railway auto-detects Python/Dockerfile
3. Set environment variables (DATABASE_URL, BETTER_AUTH_SECRET)
4. Deploy automatically on git push to main

**Render Deploy**:
1. Connect GitHub repository
2. Set build command: `uv sync`
3. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
4. Set environment variables
5. Deploy

---

## Summary of Technical Decisions

| Area | Technology | Key Reason |
|------|-----------|-----------|
| **Frontend Framework** | Next.js 16+ App Router | React Server Components, best DX, Vercel integration |
| **Authentication** | Better Auth + JWT | Self-hosted, JWT support, TypeScript-first |
| **Backend API** | FastAPI (async) | High performance, type safety, auto documentation |
| **ORM** | SQLModel | Pydantic integration, type safety, less boilerplate |
| **Database** | Neon PostgreSQL | Serverless, free tier, PostgreSQL features |
| **Styling** | Tailwind CSS | Utility-first, consistent, fast development |
| **JWT Verification** | python-jose | Industry standard, secure, lightweight |
| **Filtering** | Database-level with indexes | Performance, free tier optimization |
| **Tag Autocomplete** | Database LIKE queries | Simple, fast with index, user-specific |
| **Deployment** | Vercel + Railway/Render | Free tiers, good DX, production-ready |

All decisions align with:
- ✅ Constitution principles (free-tier, stateless, YAGNI)
- ✅ Specification requirements (47 functional requirements)
- ✅ Performance goals (<200ms API, <2s UI load)
- ✅ Scale targets (50 users, 10k tasks)
