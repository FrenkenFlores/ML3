"""
API routes with authentication protection.
"""

from flask import Blueprint, jsonify, request, current_app
from auth import login_required
from database.models import get_db

# Create API blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/data', methods=['GET'])
@login_required
def get_data():
    """Protected API endpoint."""
    user = current_app.config['current_user']
    
    data = {
        'message': 'Hello from protected API',
        'status': 'success',
        'data': {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }
    }
    return jsonify(data)

@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """Get list of users (admin only)."""
    # This would require admin role checking
    db_session = next(get_db())
    users = db_session.query(User).all()
    
    user_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    } for user in users]
    
    return jsonify({
        'status': 'success',
        'data': user_list
    })

# Add API routes to app
def register_api_routes(app):
    """Register API routes with the Flask app."""
    app.register_blueprint(api_bp, url_prefix='/api')
    return app