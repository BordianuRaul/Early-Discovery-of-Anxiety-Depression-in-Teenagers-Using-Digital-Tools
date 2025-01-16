from flask import Blueprint, jsonify
from service.heuristic_service import calculate_heuristic_score
from service.model_service import predict_sentiment
from model.database import get_db

analysis_bp = Blueprint('analysis_routes', __name__)

@analysis_bp.route('/analyze_user/<int:user_id>', methods=['GET'])
def analyze_user(user_id):
    """
    Analyze the user's data, including reactions and created content, predict sentiments,
    and compute the heuristic score.
    """
    db = get_db()
    cursor = db.cursor()

    # Fetch user-generated posts and comments
    cursor.execute("SELECT title FROM posts WHERE user_id = ?", (user_id,))
    posts = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT body FROM comments WHERE user_id = ?", (user_id,))
    comments = [row[0] for row in cursor.fetchall()]

    # Fetch upvoted reactions
    cursor.execute("SELECT title FROM reactions WHERE user_id = ?", (user_id,))
    reactions = [row[0] for row in cursor.fetchall()]

    # Validate data
    if not posts and not comments and not reactions:
        return jsonify({'error': 'No data found for this user.'}), 404

    # Use AI model to predict sentiments
    all_texts = posts + comments + reactions
    predictions = predict_sentiment(all_texts)

    # Separate predictions
    post_predictions = predictions[:len(posts)]
    comment_predictions = predictions[len(posts):len(posts) + len(comments)]
    reaction_predictions = predictions[len(posts) + len(comments):]

    # Compute heuristic score
    heuristic_result = calculate_heuristic_score(predictions)

    return jsonify({
        'user_id': user_id,
        'heuristic_score': heuristic_result['score'],
        'emotional_state': heuristic_result['emotional_state'],
        'predictions': predictions,
        'reddit_data': {
            'posts': posts,
            'comments': comments,
            'reactions': reactions,
            'post_predictions': post_predictions,
            'comment_predictions': comment_predictions,
            'reaction_predictions': reaction_predictions
        }
    }), 200
