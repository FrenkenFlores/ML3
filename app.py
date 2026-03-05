"""
Main Flask application with authentication system.
"""

from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
from flask_session import Session
import os
from database.models import Base, engine, get_db
from database.init_db import init_db
from config import SECRET_KEY, FLASK_ENV
from routes.auth_routes import register_auth_routes
from routes.main_routes import register_main_routes
from routes.api_routes import register_api_routes
from auth import login_required

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Initialize session
Session(app)

# Initialize database
Base.metadata.create_all(bind=engine)
init_db()

# Register routes
register_main_routes(app)
register_auth_routes(app)
register_api_routes(app)

@app.context_processor
def inject_user():
    """Inject user information into templates."""
    if session.get('logged_in'):
        return {
            'current_user': {
                'user_id': session.get('user_id'),
                'username': session.get('username'),
                'email': session.get('email'),
                'logged_in': True
            }
        }
    return {'current_user': {'logged_in': False}}

@app.route('/protected')
@login_required
def protected():
    """Example protected route."""
    return render_template('protected.html')

if __name__ == '__main__':
    app.run(debug=FLASK_ENV == 'development', host='0.0.0.0', port=5009)