"""
Authentication utilities for user login and registration system.
"""

import bcrypt
from datetime import datetime, timedelta
from flask import session, redirect, url_for, request, flash
from database.models import User, get_db
from config import SECRET_KEY

# Password hashing utility
class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        """Verify a password against a stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

# Session management
class SessionManager:
    @staticmethod
    def login_user(user_id: int, username: str, email: str):
        """Create a user session."""
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = email
        session['logged_in'] = True
        session.permanent = True
        
    @staticmethod
    def logout_user():
        """Clear the user session."""
        session.clear()
    
    @staticmethod
    def is_logged_in() -> bool:
        """Check if user is logged in."""
        return session.get('logged_in', False)
    
    @staticmethod
    def get_current_user() -> dict:
        """Get current user information."""
        if SessionManager.is_logged_in():
            return {
                'user_id': session.get('user_id'),
                'username': session.get('username'),
                'email': session.get('email')
            }
        return None

# Authentication routes
class AuthRoutes:
    @staticmethod
    def register(username: str, email: str, password: str, db_session):
        """Register a new user."""
        # Validate input
        if not username or not email or not password:
            return {'success': False, 'message': 'All fields are required'}
        
        if len(password) < 8:
            return {'success': False, 'message': 'Password must be at least 8 characters'}
        
        # Check if user already exists
        existing_user = db_session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                return {'success': False, 'message': 'Username already exists'}
            if existing_user.email == email:
                return {'success': False, 'message': 'Email already exists'}
        
        # Create new user
        hashed_password = PasswordUtils.hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        
        db_session.add(new_user)
        db_session.commit()
        
        return {'success': True, 'message': 'Registration successful', 'user_id': new_user.id}
    
    @staticmethod
    def login(email: str, password: str, db_session):
        """Login an existing user."""
        # Validate input
        if not email or not password:
            return {'success': False, 'message': 'Email and password are required'}
        
        # Find user by email
        user = db_session.query(User).filter(User.email == email).first()
        
        if not user:
            return {'success': False, 'message': 'Invalid email or password'}
        
        # Verify password
        if not PasswordUtils.verify_password(user.password_hash, password):
            return {'success': False, 'message': 'Invalid email or password'}
        
        # Create session
        SessionManager.login_user(user.id, user.username, user.email)
        
        return {'success': True, 'message': 'Login successful', 'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }}
    
    @staticmethod
    def logout():
        """Logout the current user."""
        SessionManager.logout_user()
        return {'success': True, 'message': 'Logout successful'}

# Decorator for protected routes
def login_required(f):
    """Decorator to protect routes that require authentication."""
    def wrap(*args, **kwargs):
        if not SessionManager.is_logged_in():
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap