<<<<<<< HEAD
import sqlite3

# Database schema creation for SQLite
def initialize_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create sentiment_analysis table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            prediction TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

<<<<<<< HEAD
class SentimentAnalysis:
    """
    Represents a single sentiment analysis record.
    """
    def __init__(self, input_text, prediction):
        self.input_text = input_text
        self.prediction = prediction

    def __repr__(self):
        return f"<SentimentAnalysis(input_text='{self.input_text}', prediction='{self.prediction}')>"
=======
=======
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

>>>>>>> 2d7f90fe350b38b7d7f714a1bb23af6be6b7c538
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MoodCheck(db.Model):
    __tablename__ = 'mood_checks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
<<<<<<< HEAD
    sentiment = db.Column(db.Integer, nullable=False)  # 0: Depression, 1: Anxiety, 2: Normal
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('moods', lazy=True))
>>>>>>> parent of 2d7f90f (AI model API; DB doesn't)
=======
    sentiment = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('moods', lazy=True))

class SentimentAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Link to a user
    input_text = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)  # 0: Depression, 1: Anxiety, 2: Normal
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

>>>>>>> 2d7f90fe350b38b7d7f714a1bb23af6be6b7c538
