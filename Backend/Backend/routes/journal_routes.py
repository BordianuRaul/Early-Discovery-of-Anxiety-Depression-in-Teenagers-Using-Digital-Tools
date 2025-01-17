from flask import Blueprint, request, jsonify, g, current_app
from model.database import get_db
from service.model_service import predict_sentiment

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/addJournalDay', methods=['POST'])
def add_journal_day():
    data = request.get_json()
    user_id = data.get('userId')
    content = data.get('content')

    if not user_id or not content:
        return jsonify({"error": "Missing userId or content"}), 400

    # Predict sentiment score for the journal entry
    sentiment_score = predict_sentiment([content])[0]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO journals (user_id, content, sentiment_score) VALUES (?, ?, ?)',
        (user_id, content, sentiment_score)
    )
    db.commit()

    return jsonify({"message": "Journal entry added successfully", "sentiment_score": sentiment_score}), 201
