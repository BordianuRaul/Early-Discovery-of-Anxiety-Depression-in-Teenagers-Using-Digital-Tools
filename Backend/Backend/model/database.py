import os
import sqlite3
from flask import g, current_app

from model.models import initialize_database

def init_db(app):
    """Initialize the database."""
    db_path = app.config['DATABASE']
    if not os.path.exists('instance'):
        os.makedirs('instance')
    initialize_database(db_path)

def get_db():
    """
    Get a SQLite database connection. If none exists, create one.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # Enable dictionary-like row access
    return db

def close_db(exception=None):
    """
    Close the SQLite database connection after the request ends.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
