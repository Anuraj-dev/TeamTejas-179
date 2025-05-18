from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from app.forms.auth_forms import LoginForm, RegistrationForm
from app.models.user import User
from app.extensions import db

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        # Check if user exists and password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Log the user in
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to the page the user was trying to access
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash('You have been logged in successfully!', 'success')
        return redirect(next_page)
    
    # Render login template
    return render_template('auth/login.html', form=form, title='Sign In')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        # Add user to database
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    # Render registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
