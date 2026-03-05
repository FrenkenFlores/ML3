"""
Database initialization script for logs classification app.
Sets up the SQLite database using the schema.sql file.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from database.models import Base


def init_db():
    """Initialize the database using schema.sql."""
    print("Initializing database...")
    
    # Create database engine
    engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///app.db'))
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == '__main__':
    init_db()
