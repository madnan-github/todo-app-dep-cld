from fastapi import FastAPI
from .routes import router
from .database import create_db_and_tables
from .mcp_server import start_mcp_server
from .logging_config import logger
import asyncio

app = FastAPI(title="Todo AI Chatbot API")

# Include the routes
app.include_router(router)

@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    print("Initializing database tables...")
    create_db_and_tables()

    # Start MCP server in the background
    print("Starting MCP server...")
    start_mcp_server()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)