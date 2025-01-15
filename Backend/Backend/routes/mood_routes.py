from flask import Blueprint, request, jsonify

from model.models import db, SentimentAnalysis
from service.model_AI import predict_sentiment

mood_bp = Blueprint('mood_routes', __name__)


@mood_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract JSON payload
        data = request.get_json()
        texts = data.get('sentences')
        user_id = data.get('user_id', None)

        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'Invalid input. Provide a list of sentences.'}), 400
        try:
            predictions = predict_sentiment(texts)
            for text, pred in zip(texts, predictions):
                analysis = SentimentAnalysis(user_id=user_id, input_text=text, prediction=pred)
                db.session.add(analysis)
            db.session.commit()
            return jsonify({'predictions': predictions.tolist()}),
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
