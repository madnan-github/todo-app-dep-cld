# Data Model: Full-Stack Web Todo Application

**Feature**: 002-fullstack-web
**Date**: 2025-12-28
**Database**: PostgreSQL (Neon Serverless)

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Users Table                              │
│  (Managed by Better Auth)                                        │
├─────────────────┬──────────────────────────────────────────────┤
│ id (PK)         │ string (UUID or similar)                      │
│ email           │ string (unique, not null)                     │
│ password_hash   │ string (hashed, not null)                     │
│ name            │ string (nullable)                             │
│ created_at      │ timestamp (default: now())                    │
└─────────────────┴──────────────────────────────────────────────┘
                                   │
                                   │ 1:N
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Tasks Table                              │
├─────────────────┬──────────────────────────────────────────────┤
│ id (PK)         │ integer (auto-increment)                      │
│ user_id (FK)    │ string (references users.id, indexed)        │
│ title           │ string (max 200 chars, not null)             │
│ description     │ text (max 1000 chars, nullable)              │
│ completed       │ boolean (default: false, indexed)            │
│ priority        │ enum ('high', 'medium', 'low', indexed)      │
│                 │   default: 'medium'                           │
│ created_at      │ timestamp (default: now())                    │
│ updated_at      │ timestamp (default: now(), auto-update)      │
└─────────────────┴──────────────────────────────────────────────┘
                                   │
                                   │ M:N (via TaskTags)
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TaskTags Junction Table                      │
├─────────────────┬──────────────────────────────────────────────┤
│ task_id (PK,FK) │ integer (references tasks.id, indexed)       │
│ tag_id (PK,FK)  │ integer (references tags.id, indexed)        │
│                 │ Composite primary key: (task_id, tag_id)     │
└─────────────────┴──────────────────────────────────────────────┘
                                   │
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Tags Table                               │
├─────────────────┬──────────────────────────────────────────────┤
│ id (PK)         │ integer (auto-increment)                      │
│ user_id (FK)    │ string (references users.id, indexed)        │
│ name            │ string (max 50 chars, indexed)               │
│                 │ Unique constraint: (user_id, name)           │
│ created_at      │ timestamp (default: now())                    │
└─────────────────┴──────────────────────────────────────────────┘
```

---

## Entity: User

**Purpose**: Represents an authenticated user account. Managed primarily by Better Auth.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | string | PRIMARY KEY, NOT NULL | Unique identifier (UUID from Better Auth) |
| `email` | string | UNIQUE, NOT NULL | User's email address (used for login) |
| `password_hash` | string | NOT NULL | Hashed password (bcrypt via passlib) |
| `name` | string | NULLABLE | User's display name (optional) |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Account creation timestamp |

### Validation Rules

- **Email**: Must be valid email format (regex: `^[^@]+@[^@]+\.[^@]+$`)
- **Password**: Minimum 8 characters (enforced at application level)
- **Email uniqueness**: Enforced by database UNIQUE constraint

### Relationships

- **1:N with Tasks**: One user can have many tasks
- **1:N with Tags**: One user can have many tags (user-scoped tags)

### Indexes

```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### Notes

- Better Auth manages this table's schema
- `password_hash` should never be exposed in API responses
- User deletion (if implemented) should cascade delete tasks and tags

---

## Entity: Task

**Purpose**: Represents a todo item owned by a specific user.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | integer | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| `user_id` | string | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner of the task |
| `title` | varchar(200) | NOT NULL | Task title (1-200 characters) |
| `description` | varchar(1000) | NULLABLE | Optional task description (max 1000 chars) |
| `completed` | boolean | NOT NULL, DEFAULT false, INDEXED | Completion status |
| `priority` | enum | NOT NULL, DEFAULT 'medium', INDEXED | Priority level: 'high', 'medium', 'low' |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Creation timestamp |
| `updated_at` | timestamp | NOT NULL, DEFAULT now() | Last modification timestamp |

### Validation Rules (Application Level)

From specification requirements:
- **Title**: Required, 1-200 characters, cannot be empty or whitespace-only (FR-008)
- **Description**: Optional, max 1000 characters (FR-008)
- **Priority**: Must be one of 'high', 'medium', 'low'; defaults to 'medium' (FR-017)
- **User isolation**: Tasks can only be accessed by their owner (FR-036)

### Relationships

- **N:1 with User**: Each task belongs to exactly one user
- **M:N with Tags**: Tasks can have multiple tags (via TaskTags junction)

### Indexes

```sql
-- Essential indexes for queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Composite index for common filtered queries
CREATE INDEX idx_tasks_user_completed_priority
ON tasks(user_id, completed, priority);
```

### State Transitions

```
┌─────────┐         toggle complete          ┌───────────┐
│ pending │ ────────────────────────────────▶│ completed │
│ (created) │                                 │           │
│         │◀────────────────────────────────│           │
└─────────┘      toggle complete again      └───────────┘
```

- **Initial state**: `completed = false` (pending)
- **Transition**: User can toggle `completed` flag any number of times (FR-014)
- **No restriction**: Completed tasks can be edited, deleted, or marked pending again

### Notes

- `updated_at` should be updated automatically on any modification
- Deletion is permanent (no soft delete in Phase II)
- Filtering by `user_id` is mandatory for all queries (user isolation)

---

## Entity: Tag

**Purpose**: Represents a categorical label that can be applied to multiple tasks. Tags are user-scoped (each user has their own tag namespace).

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | integer | PRIMARY KEY, AUTO_INCREMENT | Unique tag identifier |
| `user_id` | string | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner of the tag |
| `name` | varchar(50) | NOT NULL, INDEXED | Tag name (e.g., "work", "urgent") |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Tag creation timestamp |

### Validation Rules

- **Name**: Required, max 50 characters, case-insensitive uniqueness per user
- **User scope**: Tag names must be unique within a user's tags (UNIQUE constraint on `(user_id, name)`)
- **Trimming**: Leading/trailing whitespace should be trimmed at application level
- **No duplicates**: Application prevents adding the same tag twice to a task (FR-025)

### Relationships

- **N:1 with User**: Each tag belongs to exactly one user
- **M:N with Tasks**: Tags can be applied to multiple tasks (via TaskTags junction)

### Indexes

```sql
CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);
CREATE UNIQUE INDEX idx_tags_user_name ON tags(user_id, name);
```

### Notes

- Tags are created on-demand when user types a new tag name
- Tags are case-insensitive for uniqueness (handled at application level or with CITEXT)
- Unused tags (tags with no task associations) can remain in the database
- Tag autocomplete queries search by prefix: `WHERE name ILIKE 'prefix%'` (FR-022)

---

## Entity: TaskTag (Junction Table)

**Purpose**: Represents the many-to-many relationship between tasks and tags.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `task_id` | integer | FOREIGN KEY → tasks.id, PRIMARY KEY | Reference to task |
| `tag_id` | integer | FOREIGN KEY → tags.id, PRIMARY KEY | Reference to tag |

### Composite Primary Key

```sql
PRIMARY KEY (task_id, tag_id)
```

This ensures:
- A task cannot have the same tag twice
- Efficient lookups in both directions (task → tags, tag → tasks)

### Relationships

- **N:1 with Task**: Links to a task
- **N:1 with Tag**: Links to a tag

### Indexes

```sql
-- These are automatically created by the composite primary key
-- but explicitly defining for clarity:
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);
```

### Cascade Behavior

```sql
-- When a task is deleted, remove all its tag associations
ON DELETE CASCADE (task_id)

-- When a tag is deleted, remove all task associations
ON DELETE CASCADE (tag_id)
```

### Notes

- No `created_at` timestamp needed (linkage event timestamp not required)
- Inserting duplicate (task_id, tag_id) pairs should be prevented by constraint
- Queries for "tasks with tag X" require JOIN through this table

---

## Database Schema (SQL DDL)

```sql
-- Enable UUID extension (if needed for Better Auth)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (managed by Better Auth)
-- This is a simplified version; Better Auth creates its own schema
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,  -- UUID as string
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Priority enum type
CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low');

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL CHECK (LENGTH(TRIM(title)) > 0),
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT false,
    priority priority_enum NOT NULL DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tags table (user-scoped)
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, name)  -- Tag names unique per user
);

-- TaskTags junction table (many-to-many)
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- Indexes for Tasks
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_user_completed_priority ON tasks(user_id, completed, priority);

-- Indexes for Tags
CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);

-- Indexes for TaskTags (covered by primary key, but explicit for clarity)
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);

-- Function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function on task updates
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Query Patterns

### 1. Get All Tasks for User (with Filters and Sorting)

```sql
-- Base query: all tasks for a user
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC;

-- With completion filter (pending only)
SELECT * FROM tasks
WHERE user_id = $1 AND completed = false
ORDER BY created_at DESC;

-- With priority filter (high priority only)
SELECT * FROM tasks
WHERE user_id = $1 AND priority = 'high'
ORDER BY created_at DESC;

-- With search filter (title or description contains keyword)
SELECT * FROM tasks
WHERE user_id = $1
  AND (title ILIKE '%keyword%' OR description ILIKE '%keyword%')
ORDER BY created_at DESC;

-- With multiple filters combined
SELECT * FROM tasks
WHERE user_id = $1
  AND completed = false
  AND priority IN ('high', 'medium')
  AND title ILIKE '%meeting%'
ORDER BY priority DESC, created_at DESC;
```

### 2. Get Tasks with Tags (JOIN)

```sql
-- Get all tasks with their tags
SELECT
    t.id,
    t.title,
    t.completed,
    t.priority,
    t.created_at,
    ARRAY_AGG(tg.name) AS tags
FROM tasks t
LEFT JOIN task_tags tt ON t.id = tt.task_id
LEFT JOIN tags tg ON tt.tag_id = tg.id
WHERE t.user_id = $1
GROUP BY t.id
ORDER BY t.created_at DESC;
```

### 3. Filter Tasks by Tag

```sql
-- Get tasks that have a specific tag (e.g., "work")
SELECT DISTINCT t.*
FROM tasks t
JOIN task_tags tt ON t.id = tt.task_id
JOIN tags tg ON tt.tag_id = tg.id
WHERE t.user_id = $1 AND tg.name = 'work'
ORDER BY t.created_at DESC;

-- Get tasks that have ALL of multiple tags (AND logic)
SELECT t.*
FROM tasks t
WHERE t.user_id = $1
  AND t.id IN (
    SELECT tt.task_id
    FROM task_tags tt
    JOIN tags tg ON tt.tag_id = tg.id
    WHERE tg.name IN ('work', 'urgent')
    GROUP BY tt.task_id
    HAVING COUNT(DISTINCT tg.name) = 2  -- Must have both tags
  )
ORDER BY t.created_at DESC;
```

### 4. Tag Autocomplete

```sql
-- Get tags for a user matching prefix (for autocomplete)
SELECT DISTINCT tg.name
FROM tags tg
WHERE tg.user_id = $1
  AND tg.name ILIKE 'pre%'  -- Prefix matching
ORDER BY tg.name
LIMIT 10;
```

### 5. Create Task with Tags

```sql
-- Transaction: Create task and associate tags
BEGIN;

-- 1. Create the task
INSERT INTO tasks (user_id, title, description, priority)
VALUES ($1, $2, $3, $4)
RETURNING id;

-- 2. Get or create tags (upsert)
INSERT INTO tags (user_id, name)
VALUES ($1, 'work'), ($1, 'urgent')
ON CONFLICT (user_id, name) DO NOTHING
RETURNING id;

-- 3. Associate task with tags
INSERT INTO task_tags (task_id, tag_id)
SELECT $task_id, id FROM tags
WHERE user_id = $1 AND name IN ('work', 'urgent');

COMMIT;
```

---

## Data Constraints Summary

| Constraint Type | Entity | Rule | Enforced By |
|-----------------|--------|------|-------------|
| **Uniqueness** | User | Email must be unique | Database (UNIQUE) |
| **Uniqueness** | Tag | (user_id, name) must be unique | Database (COMPOSITE UNIQUE) |
| **Uniqueness** | TaskTag | (task_id, tag_id) must be unique | Database (PRIMARY KEY) |
| **Length** | Task.title | 1-200 characters | Application + Database (CHECK) |
| **Length** | Task.description | Max 1000 characters | Application + Database (VARCHAR) |
| **Length** | Tag.name | Max 50 characters | Application + Database (VARCHAR) |
| **Referential** | Task.user_id | Must reference existing user | Database (FOREIGN KEY) |
| **Referential** | Tag.user_id | Must reference existing user | Database (FOREIGN KEY) |
| **Referential** | TaskTag.task_id | Must reference existing task | Database (FOREIGN KEY) |
| **Referential** | TaskTag.tag_id | Must reference existing tag | Database (FOREIGN KEY) |
| **Enum** | Task.priority | Must be 'high', 'medium', or 'low' | Database (ENUM TYPE) |
| **NOT NULL** | Task.title | Cannot be null or empty | Database + Application |
| **User Isolation** | All queries | user_id filter mandatory | Application (enforced in code) |

---

## Performance Considerations

### Index Usage

| Query Type | Indexes Used | Expected Performance |
|------------|--------------|---------------------|
| List user tasks | `idx_tasks_user_id` | <50ms for 500 tasks |
| Filter by completion | `idx_tasks_user_completed_priority` (composite) | <100ms |
| Filter by priority | `idx_tasks_user_completed_priority` (composite) | <100ms |
| Search by keyword | Full table scan (no text index) | <200ms for 500 tasks |
| Sort by created_at | `idx_tasks_created_at` | <50ms |
| Tag autocomplete | `idx_tags_name` | <20ms |
| Tasks with tag | `idx_task_tags_tag_id` + `idx_task_tags_task_id` | <100ms |

### Scalability Notes

- **Current design**: Optimized for per-user queries (up to 500 tasks per user)
- **Free-tier limits**: Neon 0.5GB storage = ~50,000 tasks (estimate: 10KB per task with tags)
- **Bottlenecks**: Full-text search without index (acceptable for small datasets)
- **Future optimization**: If search becomes slow, add PostgreSQL full-text search index

---

## Migration Strategy

### Phase I → Phase II Migration

Phase I used in-memory dictionary storage. Phase II requires database migration:

1. **No data migration needed**: Phase I and Phase II are separate codebases
2. **Schema creation**: Run DDL script to create tables (Better Auth will create users table)
3. **Initial data**: Start with empty database (users create new accounts)

### Alembic Migrations (Optional)

For future schema changes, use Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "Add due_date to tasks"

# Apply migration
alembic upgrade head
```

---

## Summary

**Total Tables**: 4 (users, tasks, tags, task_tags)
**Total Indexes**: 10 (covering all common queries)
**Relationships**: 3 (User→Tasks, User→Tags, Tasks↔Tags via junction)
**Constraints**: 14 (uniqueness, foreign keys, NOT NULL, CHECK, enum)

This data model satisfies:
- ✅ All 47 functional requirements from specification
- ✅ User isolation (every query filters by user_id)
- ✅ Performance goals (<200ms API responses)
- ✅ Free-tier constraints (efficient indexes reduce compute usage)
- ✅ Scalability targets (500 tasks per user, 50 users)
