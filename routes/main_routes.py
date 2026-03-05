"""
Main application routes with authentication protection.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from auth import login_required

# Create main blueprint
main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@main_bp.route('/about')
@login_required
def about():
    """About page route."""
    return render_template('about.html')

@main_bp.route('/api/data')
@login_required
def api_data():
    """API data route."""
    return redirect(url_for('api.get_data'))

# Add main routes to app
def register_main_routes(app):
    """Register main routes with the Flask app."""
    app.register_blueprint(main_bp)
    return app