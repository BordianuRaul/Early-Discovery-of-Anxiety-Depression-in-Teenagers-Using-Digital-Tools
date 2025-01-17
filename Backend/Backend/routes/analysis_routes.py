from flask import Blueprint, jsonify
from service.heuristic_service import calculate_heuristic_score
from service.model_service import predict_sentiment
from model.database import get_db

analysis_bp = Blueprint('analysis_routes', __name__)

@analysis_bp.route('/analyze_user/<user_id>', methods=['GET'])
def analyze_user(user_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch user-generated posts, comments, and journal entries
    cursor.execute("SELECT title FROM posts WHERE user_id = ?", (user_id,))
    posts = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT body FROM comments WHERE user_id = ?", (user_id,))
    comments = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT content, sentiment_score FROM journals WHERE user_id = ?", (user_id,))
    journals = [{"content": row[0], "sentiment_score": row[1]} for row in cursor.fetchall()]

    # Fetch upvoted reactions
    cursor.execute("SELECT title FROM reactions WHERE user_id = ?", (user_id,))
    reactions = [row[0] for row in cursor.fetchall()]

    # Validate data
    if not posts and not comments and not journals and not reactions:
        return jsonify({'error': 'No data found for this user.'}), 404

    # Use AI model to predict sentiments for posts, comments, and reactions
    all_texts = posts + comments + reactions
    predictions = predict_sentiment(all_texts)

    # Separate predictions
    post_predictions = predictions[:len(posts)]
    comment_predictions = predictions[len(posts):len(posts) + len(comments)]
    reaction_predictions = predictions[len(posts) + len(comments):]

    # Add journal sentiments to the heuristic calculation
    journal_scores = [journal['sentiment_score'] for journal in journals]
    print(journal_scores)
    all_scores = post_predictions + comment_predictions + reaction_predictions + journal_scores

    # Compute heuristic score
    heuristic_result = calculate_heuristic_score(all_scores, journal_scores)

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
        },
        'journals': journals
    }), 200

