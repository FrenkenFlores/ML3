"""
Configuration file for logs classification app.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/logs_classification')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ml3')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')

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
else:
    DEBUG = False
    TESTING = False

# Security settings
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_MINUTES = 30

# Email configuration
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Celery configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# ML model configuration
MODEL_PATH = BASE_DIR / 'models' / 'classification_model.pkl'
MODEL_PATH.mkdir(parents=True, exist_ok=True)

# Default label colors
DEFAULT_LABEL_COLORS = {
    'Error': '#dc3545',
    'Warning': '#ffc107',
    'Info': '#17a2b8',
    'Debug': '#6c757d',
    'Critical': '#343a40'
}

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100