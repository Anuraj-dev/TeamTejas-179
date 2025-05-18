from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

# Create blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route."""
    # User dashboard will be handled by teammates
    return render_template('user/dashboard.html', title='Dashboard')

@user_bp.route('/profile')
@login_required
def profile():
    """User profile route."""
    # User profile will be handled by teammates
    return render_template('user/profile.html', title='My Profile')

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile route."""
    # Profile editing will be handled by teammates
    if request.method == 'POST':
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html', title='Edit Profile')
