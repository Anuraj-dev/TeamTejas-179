from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc

from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.forms.product_forms import ProductForm, ProductEditForm

# Create blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def index():
    """List all products."""
    # Get query parameters for filtering and sorting
    category_id = request.args.get('category', type=int)
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of products per page
    
    # Base query - only active products that are not sold
    query = Product.query.filter_by(is_active=True, is_sold=False)
    
    # Apply category filter if provided
    if category_id:
        query = query.filter_by(category_id=category_id)
        category = Category.query.get(category_id)
    else:
        category = None
    
    # Apply sorting
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    else:  # 'newest' is default
        query = query.order_by(desc(Product.created_at))
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    # Get all categories for the filter
    categories = Category.query.all()
    
    return render_template('products/listing.html', 
                          title='Products',
                          products=products,
                          pagination=pagination,
                          categories=categories,
                          category=category)

@products_bp.route('/<int:product_id>')
def view(product_id):
    """View a single product."""
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', title=product.title, product=product)

@products_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new product listing."""
    form = ProductForm()
    
    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    
    if form.validate_on_submit():
        # Create new product
        product = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category_id.data,
            seller_id=current_user.id,
            is_active=True,
            is_sold=False
        )
        
        # Handle image upload
        if form.image.data:
            try:
                filename = secure_filename(form.image.data.filename)
                # Create unique filename to prevent overwriting
                unique_filename = f"{product.id or 'new'}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', unique_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                form.image.data.save(filepath)
                product.image_url = f"/static/images/uploads/products/{unique_filename}"
            except Exception as e:
                flash(f'Error uploading product image: {str(e)}', 'danger')
        
        try:
            # Save to database
            db.session.add(product)
            db.session.commit()
            flash('Product created successfully!', 'success')
            return redirect(url_for('products.view', product_id=product.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating product: {str(e)}', 'danger')
    
    # If form validation failed
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return render_template('products/create.html', title='Create Listing', form=form, categories=Category.query.all())

@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(product_id):
    """Edit a product listing."""
    # Get product and verify ownership
    product = Product.query.get_or_404(product_id)
    
    if product.seller_id != current_user.id:
        flash('You do not have permission to edit this listing.', 'danger')
        return redirect(url_for('products.view', product_id=product.id))
    
    form = ProductEditForm(obj=product)
    
    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    
    if request.method == 'GET':
        return render_template('products/edit.html', title='Edit Listing', form=form, product=product, categories=Category.query.all())
    
    if form.validate_on_submit():
        # Update product
        product.title = form.title.data
        product.description = form.description.data
        product.price = form.price.data
        product.category_id = form.category_id.data
        product.is_active = form.is_active.data
        product.is_sold = form.is_sold.data
        
        # Handle image upload or deletion
        if form.delete_image.data and product.image_url:
            # Remove the image URL (not physically deleting the file)
            product.image_url = None
        elif form.image.data:
            try:
                filename = secure_filename(form.image.data.filename)
                # Create unique filename
                unique_filename = f"{product.id}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', unique_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                form.image.data.save(filepath)
                product.image_url = f"/static/images/uploads/products/{unique_filename}"
            except Exception as e:
                flash(f'Error uploading product image: {str(e)}', 'danger')
        
        try:
            # Save changes to database
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products.view', product_id=product.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'danger')
    
    # If form validation failed
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return render_template('products/edit.html', title='Edit Listing', form=form, product=product, categories=Category.query.all())

@products_bp.route('/<int:product_id>/delete', methods=['POST'])
@login_required
def delete(product_id):
    """Delete a product listing."""
    product = Product.query.get_or_404(product_id)
    
    # Verify ownership
    if product.seller_id != current_user.id:
        flash('You do not have permission to delete this listing.', 'danger')
        return redirect(url_for('products.view', product_id=product.id))
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully.', 'success')
        return redirect(url_for('products.my_listings'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')
        return redirect(url_for('products.view', product_id=product.id))

@products_bp.route('/my-listings')
@login_required
def my_listings():
    """View current user's listings."""
    return render_template('products/my_listings.html', title='My Listings')

@products_bp.route('/search')
def search():
    """Search for products."""
    query = request.args.get('q', '')
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    if not query:
        return redirect(url_for('products.index'))
    
    # Search in title and description
    search_query = Product.query.filter(
        (Product.title.ilike(f'%{query}%') | Product.description.ilike(f'%{query}%')) &
        (Product.is_active == True) &
        (Product.is_sold == False)
    )
    
    # Apply sorting
    if sort == 'price_low':
        search_query = search_query.order_by(Product.price.asc())
    elif sort == 'price_high':
        search_query = search_query.order_by(Product.price.desc())
    else:  # 'newest' is default
        search_query = search_query.order_by(desc(Product.created_at))
    
    # Paginate results
    pagination = search_query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    # Get all categories for the filter
    categories = Category.query.all()
    
    return render_template(
        'products/listing.html', 
        title=f'Search: {query}',
        products=products,
        pagination=pagination,
        categories=categories,
        category=None,
        search_query=query
    )
