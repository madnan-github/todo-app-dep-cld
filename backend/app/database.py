from sqlmodel import create_engine, Session
from typing import Generator
from .models import SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session