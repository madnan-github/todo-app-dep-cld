# TaskFlow - Full-Stack AI-Powered Todo Application

A modern, full-stack AI-powered todo application built with Next.js 15, FastAPI, and PostgreSQL. Users can manage their tasks using natural language commands through an AI assistant. This project demonstrates the evolution from a simple console app to a cloud-native AI system using Spec-Driven Development.

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
- **Advanced Features** - Recurring tasks, due dates & reminders, event-driven architecture
- **Cloud Native** - Deployed on Kubernetes with Dapr for distributed systems

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
- **PostgreSQL** (Local or Neon serverless)
- **JWT** for authentication

### AI & Tools
- **OpenAI Agents SDK** - Agent development framework
- **MCP (Model Context Protocol)** - Tool server for task operations
- **OpenRouter API** - Claude AI model for natural language processing

### Cloud & Infrastructure
- **Docker** - Containerization
- **NeonDB** - Serverless PostgreSQL for cloud deployment
- **Kubernetes** - Orchestration (Minikube, AKS, GKE, DOKS)
- **Helm Charts** - Package management
- **Dapr** - Distributed Application Runtime
- **Kafka** - Event streaming platform
- **kubectl-ai** - AI-assisted Kubernetes operations
- **kagent** - AI-powered cluster analysis

## The Evolution of Todo: 5-Phase Journey

### Phase I: Todo In-Memory Python Console App
- **Objective**: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus
- **Features**: Add, Delete, Update, View, Mark Complete tasks
- **Tech Stack**: Python 3.13+, UV, Claude Code, Spec-Kit Plus
- **Architecture**: Simple console application with in-memory storage

### Phase II: Todo Full-Stack Web Application
- **Objective**: Transform the console app into a modern multi-user web application with persistent storage
- **Features**: All Phase I features plus user authentication, responsive UI, persistent storage
- **Tech Stack**: 
  - Frontend: Next.js 15+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth
- **API Endpoints**: RESTful API with JWT authentication

### Phase III: Todo AI Chatbot
- **Objective**: Create an AI-powered chatbot interface for managing todos through natural language
- **Features**: Conversational interface for all task operations using natural language
- **Tech Stack**:
  - Frontend: OpenAI ChatKit
  - Backend: Python FastAPI
  - AI Framework: OpenAI Agents SDK
  - MCP Server: Official MCP SDK
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
- **Architecture**: Stateless chat endpoint with MCP tools for task operations

### Phase IV: Local Kubernetes Deployment
- **Objective**: Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube and Helm Charts
- **Features**: Containerized applications with Kubernetes orchestration
- **Tech Stack**:
  - Containerization: Docker, Docker AI Agent (Gordon)
  - Orchestration: Kubernetes (Minikube)
  - Package Manager: Helm Charts
  - AI DevOps: kubectl-ai, kagent
- **Deployment**: Local Kubernetes cluster with AI-assisted operations

### Phase V: Advanced Cloud Deployment
- **Objective**: Deploy to production-grade Kubernetes with advanced features and event-driven architecture
- **Features**: Advanced features (recurring tasks, due dates), event-driven architecture with Kafka, Dapr integration
- **Tech Stack**:
  - Cloud Platforms: Azure (AKS), Google Cloud (GKE), Oracle (OKE)
  - Event Streaming: Kafka/Redpanda Cloud
  - Distributed Runtime: Dapr
  - CI/CD: GitHub Actions
  - Monitoring: Cloud-native observability tools

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (Neon free tier recommended)
- OpenRouter API key (for AI functionality)
- Docker Desktop
- Minikube (for local Kubernetes)
- kubectl

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

### Docker Compose Setup

```bash
# Start the complete application with Docker Compose
docker-compose up -d

# Access the application:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - Backend API Docs: http://localhost:8000/docs
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
OPENROUTER_API_KEY=your-openrouter-api-key
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

## MCP Tools Specification

The MCP server exposes the following tools for the AI agent:

### add_task
- **Purpose**: Create a new task
- **Parameters**: user_id (string, required), title (string, required), description (string, optional)
- **Returns**: task_id, status, title

### list_tasks
- **Purpose**: Retrieve tasks from the list
- **Parameters**: user_id (string, required), status (string, optional: "all", "pending", "completed")
- **Returns**: Array of task objects

### complete_task
- **Purpose**: Mark a task as complete
- **Parameters**: user_id (string, required), task_id (integer, required)
- **Returns**: task_id, status, title

### delete_task
- **Purpose**: Remove a task from the list
- **Parameters**: user_id (string, required), task_id (integer, required)
- **Returns**: task_id, status, title

### update_task
- **Purpose**: Modify task title or description
- **Parameters**: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
- **Returns**: task_id, status, title

## Dapr Integration

This application leverages Dapr (Distributed Application Runtime) for cloud-native development:

### Dapr Building Blocks Used
- **Pub/Sub**: Kafka abstraction for event streaming
- **State Management**: Conversation state storage
- **Service Invocation**: Inter-service communication with retries
- **Bindings**: Cron triggers for scheduled reminders
- **Secrets Management**: Secure storage of API keys and credentials

### Dapr Components
- `kafka-pubsub`: Event streaming (task-events, reminders)
- `statestore`: PostgreSQL-based state management
- `scheduler`: Job scheduling for reminders
- `kubernetes-secrets`: Secure credential storage

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

### Local PostgreSQL Deployment

1. Use the default configuration to run with local PostgreSQL:
   ```bash
   docker-compose up -d
   ```
2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### NeonDB Deployment

1. To use NeonDB instead of local PostgreSQL, use the neon configuration:
   ```bash
   docker-compose -f docker-compose.neon.yml up -d
   ```
2. The application will connect to NeonDB and store data in the cloud database
3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Local Kubernetes (Minikube)

1. Install Minikube and kubectl
2. Start Minikube: `minikube start`
3. Install Dapr: `dapr init -k`
4. Deploy with Helm: `helm install todo-app ./charts/todo-app`
5. Access the application: `minikube service todo-app-frontend`

### Cloud Deployment (AKS/GKE)

1. Set up your cloud Kubernetes cluster
2. Configure kubectl to connect to your cluster
3. Install Dapr: `dapr init -k`
4. Deploy with Helm: `helm install todo-app ./charts/todo-app --set global.host=your-domain.com`
5. Configure ingress and SSL certificates

## Project Structure

```
todo-app/
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
├── charts/                   # Helm charts for Kubernetes deployment
│   └── todo-app/            # Helm chart for the entire application
├── specs/                    # Specifications for spec-driven development
│   ├── overview.md          # Project overview
│   ├── architecture.md      # System architecture
│   ├── features/            # Feature specifications
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/                 # API specifications
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   └── database/            # Database specifications
│       └── schema.md
├── k8s/                      # Kubernetes manifests
│   ├── deployment.yaml      # Application deployments
│   ├── service.yaml         # Service definitions
│   └── ingress.yaml         # Ingress configuration
├── .specify/                 # Spec-Kit configuration
├── docker-compose.yml       # Docker Compose configuration (local PostgreSQL)
├── docker-compose.neon.yml  # Docker Compose configuration (NeonDB)
├── kubectl-ai-simulated-output.yaml # AI-assisted Kubernetes examples
├── DEPLOYMENT.md            # Detailed deployment instructions
├── PRODUCTION-SETUP.md      # Production environment setup
├── DB_CONFIG.md             # Database configuration guide
├── AI_DEVOPS_INTEGRATION_SUMMARY.md # AI DevOps integration details
├── CLAUDE.md                # Claude Code instructions
├── AGENTS.md                # AI agent behavior specifications
└── README.md                # This file
```

## Spec-Driven Development

This project follows a Spec-Driven Development approach using Claude Code and Spec-Kit Plus:

1. **Specify**: Define requirements in `/specs/` directory
2. **Plan**: Create technical approach in `speckit.plan`
3. **Tasks**: Break down implementation in `speckit.tasks`
4. **Implement**: Write code following the specifications

### Key Benefits
- Clear requirements before implementation
- Predictable development process
- Easy collaboration between AI agents and humans
- Traceability from requirements to code

## AI DevOps Integration

This project integrates AI tools for DevOps operations:

- **kubectl-ai**: AI-assisted Kubernetes operations
- **kagent**: AI-powered cluster analysis and optimization
- **Docker AI Agent (Gordon)**: Intelligent Docker operations
- **Spec-Kit Plus**: Specification management with AI assistance

## Event-Driven Architecture

Advanced features use Kafka for event-driven architecture:

- **Reminder/Notification System**: Scheduled reminders via Kafka events
- **Recurring Task Engine**: Auto-creation of recurring tasks
- **Activity/Audit Log**: Complete history of all operations
- **Real-time Sync**: Cross-client synchronization

## License

MIT

## Development Philosophy

This project demonstrates progressive software architecture evolution from simple console app to cloud-native AI system. It follows a Spec-Driven Development approach with AI-first implementation, emphasizing:

- Clean architecture principles
- Event-driven design
- Cloud-native patterns
- AI-assisted development
- Comprehensive testing
- Production-ready deployment

## Hackathon Information

This project is part of "Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI", focusing on:

- Spec-Driven Development using Claude Code and Spec-Kit Plus
- Reusable Intelligence: Agents Skills and Subagent Development
- Full-Stack Development with Next.js, FastAPI, SQLModel, and Neon Serverless Database
- AI Agent Development using OpenAI Agents SDK and Official MCP SDK
- Cloud-Native Deployment with Docker, Kubernetes, Minikube, and Helm Charts
- Event-Driven Architecture using Kafka and Dapr
- AIOps with kubectl-ai, kagent and Claude Code
- Development of Cloud-Native Blueprints for Spec-Driven Deployment
