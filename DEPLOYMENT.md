# Phase V: Advanced Cloud Deployment Documentation

## Overview
This document describes the implementation of Phase V for the TaskFlow application, which focuses on advanced cloud deployment with event-driven architecture using Kafka and Dapr.

## Features Implemented

### 1. Advanced Features
- **Recurring Tasks**: Tasks can be set to repeat on daily, weekly, monthly, or yearly basis
- **Due Dates & Reminders**: Tasks can have due dates with automated reminder notifications
- **Enhanced Task Properties**: Priority levels, due dates, recurrence patterns

### 2. Event-Driven Architecture
- **Kafka Integration**: All task operations publish events to Kafka topics
- **Dapr Pub/Sub**: Using Dapr's pub/sub building block to abstract Kafka
- **Event Topics**:
  - `task-events`: General task operations (create, update, delete)
  - `task-reminders`: Reminder notifications
  - `task-recurring`: Recurring task triggers
  - `task-audit`: Audit trail for compliance

### 3. Dapr Integration
- **Pub/Sub Building Block**: Abstracts Kafka messaging
- **State Management**: Redis-backed state store
- **Service Invocation**: Inter-service communication
- **Secrets Management**: Secure credential handling
- **Configuration**: Dapr configuration for observability

## Architecture

### System Components
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │────│   Backend   │────│   Database  │
│   (Next.js) │    │  (FastAPI)  │    │  (PostgreSQL)│
└─────────────┘    └─────────────┘    └─────────────┘
                    │           │
              ┌─────▼───────────▼─────┐
              │      Dapr Sidecar     │
              │   (Pub/Sub, State)    │
              └───────────────────────┘
                           │
                   ┌───────▼────────┐
                   │   Kafka/Redpanda  │
                   │   Event Stream    │
                   └──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐  ┌─────▼──────┐   ┌──────▼──────────┐
│ Notification   │  │ Recurring  │   │ Audit Service   │
│ Service        │  │ Task       │   │                 │
└────────────────┘  │ Service    │   └─────────────────┘
                    └────────────┘
```

### Data Model Changes
Added to the `Task` model:
- `due_date`: DateTime when the task is due
- `reminder_sent`: Boolean flag indicating if reminder was sent
- `is_recurring`: Boolean flag for recurring tasks
- `recurrence_pattern`: Enum (DAILY, WEEKLY, MONTHLY, YEARLY)
- `recurrence_interval`: Integer interval for recurrence
- `next_occurrence`: DateTime for next occurrence
- `parent_task_id`: Foreign key linking to parent task for recurring tasks

## Implementation Details

### Backend Changes

#### Models (`src/models.py`)
- Extended `Task` model with advanced features fields
- Added `RecurrencePatternEnum` for recurrence types
- Added `TaskEvent` model for event tracking

#### Schemas (`src/schemas.py`)
- Updated `TaskCreate`, `TaskUpdate`, and `TaskResponse` with new fields
- Added validation for recurrence intervals

#### Routes (`src/routes/tasks.py`)
- Enhanced task endpoints with due date and recurrence support
- Added reminder endpoint
- Integrated Dapr client for event publishing
- Added advanced filtering and sorting options

#### Kafka Integration (`src/kafka_producer.py`, `src/kafka_consumer.py`)
- Producer for publishing task events to Kafka
- Consumer for processing incoming events
- Separate handling for reminders, recurring tasks, and audit events

#### Dapr Integration (`src/dapr_client.py`)
- Client for interacting with Dapr services
- Methods for pub/sub, state management, service invocation, and secrets

#### Background Tasks (`src/background_tasks.py`)
- Manager for handling recurring tasks and reminders
- Processes due reminders
- Creates recurring task instances
- Processes stored task events

### Dapr Components
Located in `backend/dapr/`:
- `kafka-pubsub.yaml`: Kafka pub/sub component
- `statestore.yaml`: Redis state store component
- `secrets.yaml`: Kubernetes secrets store
- `config.yaml`: Dapr configuration

### Kubernetes Manifests
Located in `kubernetes/`:
- `backend-deployment.yaml`: Backend deployment with Dapr sidecar
- `frontend-deployment.yaml`: Frontend deployment with Dapr sidecar
- `kafka-cluster.yaml`: Strimzi Kafka cluster
- `kafka-topics.yaml`: Kafka topics for task events
- `redis-deployment.yaml`: Redis for Dapr state store

## Deployment

### Prerequisites
- Minikube
- kubectl
- Dapr CLI
- Docker

### Deployment Steps
1. Run the deployment script: `./start-all-features.sh`
2. The script will:
   - Start Minikube if not running
   - Install Dapr to the cluster
   - Install Strimzi Kafka operator
   - Deploy Kafka cluster and topics
   - Deploy Redis for state management
   - Build and deploy application containers
   - Deploy Dapr components

### Accessing Services
- Frontend: `minikube service taskflow-frontend-service --url`
- Backend API: `minikube service taskflow-backend-service --url`
- API Documentation: `/docs` endpoint on backend

## Testing

### Manual Testing
1. Create a recurring task with due date
2. Verify the task appears in the UI
3. Check Kafka topics for published events
4. Verify recurring task creates new instances
5. Test reminder functionality

### Verification Commands
```bash
# Check pods
kubectl get pods

# Check services
kubectl get svc

# View application logs
kubectl logs -l app=taskflow-backend
kubectl logs -l app=taskflow-frontend

# View Dapr logs
kubectl logs -l app=dapr-placement-server
```

## Monitoring and Observability

### Health Checks
- Backend: `/api/health` endpoint reports database and Kafka status
- Dapr: Built-in health checks for sidecars

### Logging
- Structured logging in both backend and Dapr components
- Centralized logging when deployed to cloud platforms

## Future Enhancements

### Planned Features
- Advanced scheduling with cron expressions
- More sophisticated recurrence patterns
- Integration with calendar services
- Enhanced audit capabilities
- Performance optimizations for large datasets

### Scaling Considerations
- Horizontal pod autoscaling based on load
- Kafka partitioning strategies
- Database connection pooling
- Caching layer implementation

## Troubleshooting

### Common Issues
1. **Dapr sidecar not starting**: Ensure Dapr is installed in the cluster
2. **Kafka connection issues**: Verify Kafka cluster is ready before deploying applications
3. **Database connection failures**: Check database credentials in secrets
4. **Event processing delays**: Monitor Kafka consumer lag

### Debugging Commands
```bash
# Check Dapr status
dapr status -k

# List Dapr components
dapr components -k

# Get detailed pod information
kubectl describe pod <pod-name>

# Port forward to access services locally
kubectl port-forward svc/taskflow-backend-service 8080:80
```

## Conclusion

Phase V successfully implements advanced cloud-native features for the TaskFlow application, including event-driven architecture with Kafka, Dapr for distributed application runtime, and comprehensive recurring task and reminder functionality. The solution is designed for scalability and maintainability in cloud environments.