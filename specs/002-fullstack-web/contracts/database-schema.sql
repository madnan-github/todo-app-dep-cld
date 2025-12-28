-- ============================================================================
-- TaskFlow Database Schema (Phase II: Full-Stack Web Application)
-- Database: PostgreSQL 15+ (Neon Serverless)
-- Created: 2025-12-28
-- ============================================================================

-- Enable UUID extension (if needed for Better Auth)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

-- Priority enum for tasks
CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low');

-- ============================================================================
-- TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Users Table (Managed by Better Auth)
-- ----------------------------------------------------------------------------
-- This is a simplified representation. Better Auth may create additional
-- fields for session management, email verification, etc.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,  -- UUID as string from Better Auth
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Tasks Table
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- Tags Table (User-scoped)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, name)  -- Tag names must be unique per user
);

-- ----------------------------------------------------------------------------
-- TaskTags Junction Table (Many-to-Many: Tasks ↔ Tags)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Tasks indexes (for filtering, sorting, and user isolation)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Composite index for common filtered queries (user + completion + priority)
CREATE INDEX idx_tasks_user_completed_priority
    ON tasks(user_id, completed, priority);

-- Tags indexes (for autocomplete and lookups)
CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);

-- TaskTags indexes (covered by primary key, but explicit for documentation)
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);

-- ============================================================================
-- TRIGGERS & FUNCTIONS
-- ============================================================================

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function before task updates
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SAMPLE DATA (for testing/development)
-- ============================================================================

-- Note: This is commented out by default. Uncomment to insert sample data.

/*
-- Sample user (password: "password123" - hashed with bcrypt)
INSERT INTO users (id, email, password_hash, name) VALUES
('test-user-1', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7u9cXhfZ.i', 'Test User');

-- Sample tasks
INSERT INTO tasks (user_id, title, description, priority, completed) VALUES
('test-user-1', 'Complete project documentation', 'Write comprehensive docs for Phase II implementation', 'high', false),
('test-user-1', 'Review pull requests', 'Review and approve pending PRs', 'medium', false),
('test-user-1', 'Buy groceries', 'Milk, eggs, bread, coffee', 'low', false),
('test-user-1', 'Deploy to production', 'Deploy Phase II to Vercel and Railway', 'high', true);

-- Sample tags
INSERT INTO tags (user_id, name) VALUES
('test-user-1', 'work'),
('test-user-1', 'personal'),
('test-user-1', 'urgent');

-- Sample task-tag associations
INSERT INTO task_tags (task_id, tag_id)
SELECT t.id, tg.id
FROM tasks t, tags tg
WHERE t.user_id = 'test-user-1'
  AND tg.user_id = 'test-user-1'
  AND (
    (t.title = 'Complete project documentation' AND tg.name IN ('work', 'urgent'))
    OR (t.title = 'Review pull requests' AND tg.name = 'work')
    OR (t.title = 'Buy groceries' AND tg.name = 'personal')
  );
*/

-- ============================================================================
-- DATABASE STATISTICS & MAINTENANCE
-- ============================================================================

-- Analyze tables for query optimization
ANALYZE users;
ANALYZE tasks;
ANALYZE tags;
ANALYZE task_tags;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify schema creation
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Verify indexes
-- SELECT indexname, indexdef FROM pg_indexes WHERE tablename IN ('tasks', 'tags', 'task_tags');

-- Check table row counts
-- SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users
-- UNION ALL SELECT 'tasks', COUNT(*) FROM tasks
-- UNION ALL SELECT 'tags', COUNT(*) FROM tags
-- UNION ALL SELECT 'task_tags', COUNT(*) FROM task_tags;
