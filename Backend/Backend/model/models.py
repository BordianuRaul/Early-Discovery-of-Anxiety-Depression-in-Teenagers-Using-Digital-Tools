import sqlite3

def initialize_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reddit_id TEXT UNIQUE,  -- Unique ID from Reddit
            title TEXT,
            body TEXT,
            sentiment_score REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reddit_id TEXT UNIQUE,  -- Unique ID from Reddit
            body TEXT,
            sentiment_score REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reddit_id TEXT UNIQUE,  -- Unique ID from Reddit
            title TEXT,
            vote TEXT CHECK(vote IN ('upvote', 'downvote')),
            sentiment_score REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


class User:
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"<User(username='{self.username}')>"

class Post:
    def __init__(self, user_id, title, sentiment_score):
        self.user_id = user_id
        self.title = title
        self.sentiment_score = sentiment_score

    def __repr__(self):
        return f"<Post(user_id={self.user_id}, title='{self.title}', sentiment_score={self.sentiment_score})>"

class Comment:
    def __init__(self, user_id, body, sentiment_score):
        self.user_id = user_id
        self.body = body
        self.sentiment_score = sentiment_score

    def __repr__(self):
        return f"<Comment(user_id={self.user_id}, body='{self.body}', sentiment_score={self.sentiment_score})>"

class SentimentAnalysis:
    def __init__(self, input_text, prediction):
        self.input_text = input_text
        self.prediction = prediction

    def __repr__(self):
        return f"<SentimentAnalysis(input_text='{self.input_text}', prediction='{self.prediction}')>"