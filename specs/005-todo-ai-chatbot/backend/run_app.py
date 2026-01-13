#!/usr/bin/env python3
"""
Runner script for the Todo AI Chatbot backend server
This script verifies that the application can be started properly
"""
import sys
import os

# Add the backend directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("Todo AI Chatbot - Application Startup Verification")
    print("=" * 50)

    try:
        # Import the main app to verify it loads correctly
        from app.main import app
        print("✓ Main application imported successfully")

        # Verify the main components are available
        from app.models import Task, Conversation, Message
        print("✓ Database models loaded successfully")

        from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
        print("✓ MCP server functions loaded successfully")

        from app.openrouter_agent import process_user_message
        print("✓ OpenRouter agent loaded successfully")

        from app.database import create_db_and_tables, get_session
        print("✓ Database components loaded successfully")

        from app.logging_config import logger
        print("✓ Logging configuration loaded successfully")

        from app.performance_monitor import perf_monitor, monitor_performance
        print("✓ Performance monitoring loaded successfully")

        print("\n✓ All components loaded successfully!")
        print("✓ Application is ready for deployment")
        print("\nTo start the server, run:")
        print("  uvicorn app.main:app --reload --port 8000")

    except Exception as e:
        print(f"✗ Error loading application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()