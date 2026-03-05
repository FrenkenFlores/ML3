"""
Authentication routes for user login and registration system.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.models import User, get_db
from auth import AuthRoutes, login_required
from config import SECRET_KEY

# Create auth blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Get database session
        db_session = next(get_db())
        
        # Register user
        result = AuthRoutes.register(username, email, password, db_session)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['message'], 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Get database session
        db_session = next(get_db())
        
        # Login user
        result = AuthRoutes.login(email, password, db_session)
        
        if result['success']:
            flash(result['message'], 'success')
            # Redirect to next if specified, otherwise home
            next_url = request.args.get('next') or url_for('main.index')
            return redirect(next_url)
        else:
            flash(result['message'], 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    result = AuthRoutes.logout()
    flash(result['message'], 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile route (protected)."""
    user = AuthRoutes.get_current_user()
    return render_template('auth/profile.html', user=user)

# Add auth routes to main app

def register_auth_routes(app):
    """Register authentication routes with the main Flask app."""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app