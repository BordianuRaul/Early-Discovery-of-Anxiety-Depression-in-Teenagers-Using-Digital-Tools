from flask import Blueprint, request, jsonify, current_app, g
from service.model_service import predict_sentiment
import sqlite3

from Backend.service.model_AI import predict_sentiment

mood_bp = Blueprint('mood_routes', __name__)

# Helper function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # Allows for dictionary-like access to rows
    return db

@mood_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract JSON payload
        data = request.get_json()
        texts = data.get('sentences')

        # Validate input
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'Invalid input. Provide a list of sentences.'}), 400

        # Predict sentiments using the AI model
        predictions = predict_sentiment(texts)

        # Save predictions to database
        db = get_db()
        cursor = db.cursor()
        for text, prediction in zip(texts, predictions):
            cursor.execute('''
                INSERT INTO sentiment_analysis (input_text, prediction)
                VALUES (?, ?)
            ''', (text, prediction))
        db.commit()

        # Respond with predictions
        return jsonify({'predictions': predictions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to list all database tables for debugging
@mood_bp.route('/tables', methods=['GET'])
def list_tables():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table['name'] for table in cursor.fetchall()]
        return jsonify(tables), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Close the database connection after each request
@mood_bp.teardown_app_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
