#!/bin/sh
# Shared health check script for Docker containers

set -e

# Check if the service is responding
if [ -n "$HEALTH_CHECK_URL" ]; then
    # Use curl if available, otherwise use wget
    if command -v curl >/dev/null 2>&1; then
        STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_CHECK_URL")
    elif command -v wget >/dev/null 2>&1; then
        STATUS_CODE=$(wget --spider --server-response "$HEALTH_CHECK_URL" 2>&1 | awk '/^  HTTP\// {print $2}' | tail -1)
    else
        echo "Error: Neither curl nor wget is available"
        exit 1
    fi

    if [ "$STATUS_CODE" -eq 200 ]; then
        exit 0
    else
        echo "Health check failed with status code: $STATUS_CODE"
        exit 1
    fi
else
    # Default to checking if a port is open
    if [ -n "$HEALTH_CHECK_PORT" ]; then
        if command -v nc >/dev/null 2>&1; then
            if nc -z localhost "$HEALTH_CHECK_PORT"; then
                exit 0
            else
                echo "Port $HEALTH_CHECK_PORT is not accessible"
                exit 1
            fi
        else
            # Fallback to netstat
            if netstat -tuln | grep ":$HEALTH_CHECK_PORT " >/dev/null; then
                exit 0
            else
                echo "Port $HEALTH_CHECK_PORT is not listening"
                exit 1
            fi
        fi
    else
        echo "No health check method configured"
        exit 1
    fi
fi