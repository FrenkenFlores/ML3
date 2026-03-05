"""
Configuration file for logs classification app.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ml3')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# SQLite fallback for development
if DB_HOST == 'localhost' and not os.getenv('DATABASE_URL'):
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/app.db')

# Flask configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# File upload configuration
UPLOAD_FOLDER = BASE_DIR / 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'log', 'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# API configuration
API_PREFIX = '/api'
API_VERSION = 'v1'

# CORS configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'app.log'

# Create directories if they don't exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Environment-specific settings
if FLASK_ENV == 'development':
    DEBUG = True
    TESTING = False
elif FLASK_ENV == 'testing':
    DEBUG = False
    TESTING = True