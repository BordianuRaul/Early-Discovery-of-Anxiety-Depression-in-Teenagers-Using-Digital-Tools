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


class SentimentAnalysis:
    """
    Represents a single sentiment analysis record.
    """
    def __init__(self, input_text, prediction):
        self.input_text = input_text
        self.prediction = prediction

    def __repr__(self):
        return f"<SentimentAnalysis(input_text='{self.input_text}', prediction='{self.prediction}')>"
