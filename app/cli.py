import click
from flask.cli import with_appcontext
from app.extensions import db
from app import models
import random
from datetime import datetime

def register_commands(app):
    """Register CLI commands with the Flask application."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_tables_command)
    app.cli.add_command(drop_tables_command)
    app.cli.add_command(create_dummy_data_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')

@click.command('create-tables')
@with_appcontext
def create_tables_command():
    """Create database tables."""
    db.create_all()
    click.echo('Created database tables.')

@click.command('drop-tables')
@with_appcontext
def drop_tables_command():
    """Drop database tables."""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        click.echo('Dropped all tables.')
    else:
        click.echo('Operation cancelled.')

@click.command('create-dummy-data')
@with_appcontext
def create_dummy_data_command():
    """Create dummy data for development."""
    # Check if we have any users
    if not models.User.query.first():
        click.echo("Creating dummy user...")
        user = models.User(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()
    else:
        user = models.User.query.first()
        click.echo(f"Using existing user: {user.username}")
    
    # Create categories if they don't exist
    categories = ["Electronics", "Books", "Clothing", "Home & Garden", "Sports", "Toys", "Automotive"]
    created_categories = []
    
    for cat_name in categories:
        if not models.Category.query.filter_by(name=cat_name).first():
            category = models.Category(
                name=cat_name,
                description=f"Products related to {cat_name.lower()}"
            )
            db.session.add(category)
            created_categories.append(category)
    
    db.session.commit()
    
    # Get all categories
    all_categories = models.Category.query.all()
    
    # Create dummy products
    product_titles = [
        "Smartphone X Pro", "Wireless Headphones", "Laptop Ultra", "Smart Watch",
        "Programming Book Complete Guide", "Mystery Novel Collection", "Science Fiction Anthology",
        "Designer T-shirt", "Winter Jacket", "Running Shoes", "Jeans Premium",
        "Kitchen Mixer", "Smart Home Hub", "Garden Tool Set", "Living Room Lamp",
        "Tennis Racket", "Basketball", "Fitness Tracker", "Yoga Mat",
        "Remote Control Car", "Board Game Collection", "Action Figure Set", "Building Blocks",
        "Car Cleaning Kit", "Dashboard Camera", "Tire Pressure Monitor", "Car Air Freshener"
    ]
    
    descriptions = [
        "Brand new condition with all features you need!",
        "Slightly used but in perfect working condition.",
        "Great value for the price, don't miss this deal!",
        "Top quality product, selling due to upgrade.",
        "One of a kind item that's hard to find anywhere else."
    ]
    
    image_urls = [
        "https://picsum.photos/id/1/500/500",
        "https://picsum.photos/id/20/500/500",
        "https://picsum.photos/id/30/500/500",
        "https://picsum.photos/id/40/500/500",
        "https://picsum.photos/id/50/500/500"
    ]
    
    # Create 15 products
    num_products = 15
    for i in range(num_products):
        # Pick a random title and category
        title = random.choice(product_titles)
        category = random.choice(all_categories)
        
        # Create product
        product = models.Product(
            title=f"{title} #{i+1}",
            description=random.choice(descriptions),
            price=round(random.uniform(9.99, 999.99), 2),
            image_url=random.choice(image_urls),
            category=category,
            seller=user,
            is_active=True,
            is_sold=False
        )
        db.session.add(product)
    
    db.session.commit()
    click.echo(f"Created {num_products} dummy products across {len(all_categories)} categories.") 