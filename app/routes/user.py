from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app.forms.user_forms import EditProfileForm
from app.extensions import db, bcrypt

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
    form = EditProfileForm(obj=current_user)
    
    if request.method == 'GET':
        # Pre-populate form with current user data
        return render_template('user/profile.html', title='Edit Profile', form=form, edit_mode=True)
    
    if form.validate_on_submit():
        # Check if username is already taken by another user
        if form.username.data != current_user.username:
            from app.models.user import User
            if User.query.filter_by(username=form.username.data).first():
                flash('Username is already taken.', 'danger')
                return render_template('user/profile.html', title='Edit Profile', form=form, edit_mode=True)
        
        # Check if email is already taken by another user
        if form.email.data.lower() != current_user.email:
            from app.models.user import User
            if User.query.filter_by(email=form.email.data.lower()).first():
                flash('Email is already taken.', 'danger')
                return render_template('user/profile.html', title='Edit Profile', form=form, edit_mode=True)
        
        # Update user info
        current_user.username = form.username.data
        current_user.email = form.email.data.lower()
        
        # Update password if provided
        if form.new_password.data:
            current_user.password = form.new_password.data
        
        # Handle profile image upload
        if form.profile_image.data:
            try:
                filename = secure_filename(form.profile_image.data.filename)
                # Create unique filename to prevent overwriting
                unique_filename = f"{current_user.id}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', unique_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                form.profile_image.data.save(filepath)
                current_user.profile_image = f"/static/images/uploads/profiles/{unique_filename}"
            except Exception as e:
                flash(f'Error uploading profile image: {str(e)}', 'danger')
        
        try:
            # Save changes to database
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
        
        return redirect(url_for('user.profile'))
    
    # If form validation failed
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return render_template('user/profile.html', title='Edit Profile', form=form, edit_mode=True)
