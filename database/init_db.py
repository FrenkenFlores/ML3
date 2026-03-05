#!/usr/bin/env python3
"""
Database initialization script for logs classification app.
Sets up the PostgreSQL database using the schema.sql file.
"""

import os
import sys
import psycopg2
from pathlib import Path


def get_db_connection():
    """Get database connection using environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'ml3'),
            user=os.getenv('DB_USER', 'admin'),
            password=os.getenv('DB_PASSWORD', 'admin')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def init_database():
    """Initialize the database using schema.sql."""
    print("Initializing database...")
    
    # Get database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Read schema file
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r') as file:
            schema_sql = file.read()
        
        # Execute schema
        cursor.execute(schema_sql)
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

def create_default_data():
    """Create default data (admin user, default labels)."""
    print("Creating default data...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create default admin user
        cursor.execute("""
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, ('admin', 'admin@example.com', 'pbkdf2:sha256:150000$default$default'))
        
        # Create default labels
        default_labels = [
            ('Error', 'Error logs', '#dc3545'),
            ('Warning', 'Warning logs', '#ffc107'),
            ('Info', 'Information logs', '#17a2b8'),
            ('Debug', 'Debug logs', '#6c757d'),
            ('Critical', 'Critical errors', '#343a40')
        ]
        
        for name, description, color in default_labels:
            cursor.execute("""
                INSERT INTO labels (name, description, color)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (name, description, color))
        
        conn.commit()
        print("Default data created successfully!")
        
    except Exception as e:
        print(f"Error creating default data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    """Main function to initialize database."""
    print("Logs Classification App - Database Initialization")
    print("=" * 50)
    
    # Initialize database
    init_database()
    
    # Create default data
    create_default_data()
    
    print("\nDatabase setup completed!")
    print("You can now run the application.")

if __name__ == "__main__":
    main()
