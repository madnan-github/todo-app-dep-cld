#!/bin/sh
# Shared entrypoint script for Docker containers

set -e

# Print startup information
echo "Starting application..."
echo "Container started at $(date)"

# Execute the main command
exec "$@"