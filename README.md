# TaskFlow - Full-Stack AI-Powered Todo Application

A modern, full-stack AI-powered todo application built with Next.js 15, FastAPI, and PostgreSQL. Users can manage their tasks using natural language commands through an AI assistant.

## Features

- **AI-Powered Task Management** - Add, list, update, and delete tasks using natural language commands
- **User Authentication** - Sign up, sign in, and session management with JWT tokens
- **Conversation Persistence** - Maintains conversation history for contextual understanding
- **Task Management** - Create, read, update, and delete tasks
- **Priority Levels** - High, medium, and low priority with color indicators
- **Tags** - Organize tasks with custom tags and autocomplete
- **Search** - Find tasks by keyword in title or description
- **Filter** - Filter by status, priority, and tags
- **Sort** - Sort by creation date, priority, or title
- **Responsive Design** - Works on desktop, tablet, and mobile

## Tech Stack

### Frontend
- **Next.js 15+** with App Router
- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **Better Auth** for authentication
- **OpenAI ChatKit** for AI chat interface

### Backend
- **FastAPI** (Python 3.13+)
- **SQLModel** for database ORM
- **PostgreSQL** (Neon serverless)
- **JWT** for authentication

### AI & Tools
- **OpenRouter API** - Claude AI model for natural language processing
- **MCP (Model Context Protocol)** - Tool server for task operations
- **OpenAI Agents SDK** - Agent development framework

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (Neon free tier recommended)
- OpenRouter API key (for AI functionality)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local with your configuration
# - NEXT_PUBLIC_API_URL: Your backend URL
# - BETTER_AUTH_SECRET: Generate a random secret

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Install dependencies with UV
uv pip install -r pyproject.toml

# Copy environment template
cp .env.example .env

# Edit .env with your configuration:
# - DATABASE_URL: Your Neon PostgreSQL connection string
# - JWT_SECRET_KEY: Generate a secure random key
# - CORS_ORIGINS: Add your frontend URL

# Start development server
uv run uvicorn src.main:app --reload
```

### Environment Variables

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
```

#### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/database
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/signin` - Sign in user

### Tasks
- `GET /api/v1/tasks` - List tasks (with filters, search, sort)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{task_id}` - Get task details
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `PATCH /api/v1/tasks/{task_id}/complete` - Toggle completion

### Chat (AI Assistant)
- `POST /api/{user_id}/chat` - Send message to AI assistant and get response with task operations

### Tags
- `GET /api/v1/tags` - List user's tags
- `POST /api/v1/tags` - Create new tag
- `DELETE /api/v1/tags/{tag_id}` - Delete tag

## Query Parameters

### GET /api/v1/tasks
| Parameter | Type | Description |
|-----------|------|-------------|
| `completed` | boolean | Filter by completion status |
| `priority` | string | Filter by priority (high, medium, low) - comma-separated for multiple |
| `tag_ids` | string | Filter by tag IDs - comma-separated |
| `search` | string | Search in title and description |
| `sort_by` | string | Sort field (created_at, updated_at, title, priority) |
| `sort_order` | string | Sort order (asc, desc) |
| `page` | number | Page number (default: 1) |
| `per_page` | number | Items per page (default: 20, max: 100) |

## Natural Language Commands

The AI assistant understands various natural language commands:

- **Add tasks**: "Add buy groceries", "Create task wash dishes", "New task: call mom"
- **List tasks**: "Show my tasks", "What's pending?", "Show completed tasks", "What do I have to do?"
- **Complete tasks**: "Mark task 1 complete", "Done with task 2", "Complete task 3"
- **Update tasks**: "Change task 1 to Pay bills", "Update task 3 description", "Edit task 2 title"
- **Delete tasks**: "Delete task 1", "Remove task 2", "Cancel task 3"

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Configure build command: `npm run build`
3. Set environment variables in Vercel dashboard
4. Deploy

### Backend (Render/Railway)

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r pyproject.toml`
4. Set start command: `uvicorn src.main:app`
5. Configure environment variables
6. Deploy

## Project Structure

```
todo-app-chatbot/
├── frontend/                 # Next.js frontend
│   ├── app/                 # App Router pages
│   ├── components/          # React components
│   │   └── ChatKitWrapper.tsx # AI chat interface
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities and configs
│   └── types/               # TypeScript types
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── models.py        # SQLModel entities (Task, Conversation, Message)
│   │   ├── database.py      # Database connection
│   │   ├── routes.py        # API route handlers
│   │   ├── openrouter_agent.py # AI agent integration
│   │   └── mcp_server.py    # MCP tools for task operations
│   └── .env                 # Environment variables
├── specs/                    # Specifications
│   └── 005-todo-ai-chatbot/ # Feature specs and tasks
└── README.md                # This file
```

## License

MIT

## Project Phases

This project demonstrates progressive software architecture evolution:

- **Phase I**: Console Application (Basic CRUD operations)
- **Phase II**: Full-Stack Web Application (Next.js + FastAPI + PostgreSQL)
- **Phase III**: AI Chatbot (Natural language task management) - *Current*
- **Phase IV**: Local Kubernetes (Containerization and orchestration)
- **Phase V**: Cloud Deployment (Production-ready deployment)

## Development Philosophy

This project follows a Spec-Driven Development approach with AI-first implementation. Each feature begins with a specification before implementation, ensuring clear requirements and reproducible AI-generated code.
