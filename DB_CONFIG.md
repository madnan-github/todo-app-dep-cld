# Database Configuration Guide

This document explains how to configure the TaskFlow application to use different database backends.

## Available Database Options

### 1. Local PostgreSQL (Default)

By default, the application uses a local PostgreSQL container when running with the standard `docker-compose up` command.

**Configuration:**
- Database: Local PostgreSQL container
- Connection: `postgresql+asyncpg://todo_user:todo_password@postgres:5432/todo_app`
- Use case: Development and testing

**To run with local PostgreSQL:**
```bash
docker-compose up -d
```

### 2. NeonDB (Cloud PostgreSQL)

The application can be configured to use NeonDB, a serverless PostgreSQL platform, for cloud-based data storage.

**Configuration:**
- Database: NeonDB serverless PostgreSQL
- Connection: `postgresql://neondb_owner:npg_sTVtWHiXo15L@ep-damp-wildflower-ada8vtmu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=prefer`
- Use case: Production and cloud deployment

**To run with NeonDB:**
```bash
docker-compose -f docker-compose.neon.yml up -d
```

## Database Migration

When switching from local PostgreSQL to NeonDB, the application will automatically create the necessary tables if they don't exist. The database schema remains the same across both configurations.

## Troubleshooting

### Common Issues

1. **Connection Timeout**: If you experience connection timeouts to NeonDB, ensure your network allows outbound connections to NeonDB's servers.

2. **SSL Errors**: The NeonDB configuration includes `sslmode=require` to ensure secure connections.

3. **Channel Binding Issues**: Some connection strings may include `channel_binding` parameters that are not supported by all clients. The NeonDB configuration uses `channel_binding=prefer`.

### Verifying Database Connection

You can verify the database connection by checking the application logs:
```bash
docker-compose -f docker-compose.neon.yml logs backend
```

Look for the message: `✓ Database initialized successfully`

## Environment Variables

The database connection is configured through the `DATABASE_URL` environment variable:

- Local PostgreSQL: `DATABASE_URL=postgresql+asyncpg://todo_user:todo_password@postgres:5432/todo_app`
- NeonDB: `DATABASE_URL=postgresql://neondb_owner:npg_sTVtWHiXo15L@ep-damp-wildflower-ada8vtmu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=prefer`

## Data Persistence

- **Local PostgreSQL**: Data persists in the Docker volume `todo-app-dep-loc_postgres_data`
- **NeonDB**: Data persists in the cloud NeonDB instance and is accessible from anywhere

## Switching Between Databases

To switch from one database to another:
1. Stop the current containers: `docker-compose down` or `docker-compose -f docker-compose.neon.yml down`
2. Start with the new configuration using the appropriate command above
3. The application will connect to the newly configured database