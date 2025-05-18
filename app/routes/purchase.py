from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Create blueprint
purchase_bp = Blueprint('purchase', __name__, url_prefix='/purchases')

@purchase_bp.route('/')
@login_required
def history():
    """View purchase history."""
    # Purchase history will be handled by teammates
    return render_template('purchases/history.html', title='Purchase History')

@purchase_bp.route('/<int:purchase_id>')
@login_required
def details(purchase_id):
    """View details of a specific purchase."""
    # Purchase details will be handled by teammates
    return render_template('purchases/details.html', title='Purchase Details')
