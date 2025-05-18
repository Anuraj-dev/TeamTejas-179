import click
from flask.cli import with_appcontext
from app.extensions import db
from app import models

def register_commands(app):
    """Register CLI commands with the Flask application."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_tables_command)
    app.cli.add_command(drop_tables_command)

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