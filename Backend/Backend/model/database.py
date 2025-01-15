import os
import sqlite3

from model.models import initialize_database


def init_db(app):
    """Initialize the database."""
    db_path = app.config['DATABASE']
    if not os.path.exists('instance'):
        os.makedirs('instance')
    initialize_database(db_path)