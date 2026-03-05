"""
Main application routes with authentication protection.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from auth import SessionManager
from auth import login_required

# Create main blueprint
main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
@login_required
def index():
    """Home page route."""
    
    from database.models import get_db, RawData, Dataset
    
    db = next(get_db())
    user = SessionManager.get_current_user()
    
    rawdata = db.query(RawData).filter(RawData.user_id == user["user_id"]).order_by(RawData.created_at.desc()).all()
    datasets = db.query(Dataset).filter(Dataset.user_id == user["user_id"]).order_by(Dataset.created_at.desc()).all()
    
    return render_template('home.html', rawdata=rawdata, datasets=datasets)

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

@main_bp.route('/create-dataset/<int:rawdata_id>')
@login_required
def create_dataset(rawdata_id):
    """Create a dataset from raw data."""
    from database.models import RawData, Dataset, Label
    from database import get_db
    
    db = next(get_db())
    user = SessionManager.get_current_user()
    
    # Get the raw data
    rawdata = db.query(RawData).filter(RawData.id == rawdata_id, RawData.user_id == user.id).first()
    
    if not rawdata:
        flash('Raw data not found or does not belong to you.', 'error')
        return redirect(url_for('main.index'))
    
    # Get all labels for the user
    labels = db.query(Label).all()
    
    if not labels:
        flash('No labels available. Please create a label first.', 'error')
        return redirect(url_for('main.index'))
    
    # Create dataset with first label (for now)
    dataset = Dataset(
        rawdata_id=rawdata.id,
        label_id=labels[0].id,
        user_id=user.id
    )
    db.add(dataset)
    db.commit()
    
    flash('Dataset created successfully!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/dataset/<int:dataset_id>')
@login_required
def view_dataset(dataset_id):
    """View dataset details."""
    from database.models import Dataset, RawData, Label
    from database import get_db
    
    db = next(get_db())
    user = SessionManager.get_current_user()
    
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.user_id == user.id).first()
    
    if not dataset:
        flash('Dataset not found or does not belong to you.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('dataset_details.html', dataset=dataset)

