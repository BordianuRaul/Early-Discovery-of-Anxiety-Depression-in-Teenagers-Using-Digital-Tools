from flask import Blueprint, redirect, request, url_for, session, jsonify, current_app, g
from service.reddit_service import get_auth_url, fetch_token, fetch_user_profile, fetch_user_activity, analyze_sentiment
from service.model_service import predict_sentiment
from model.models import User, Post, Comment
from model.database import get_db

reddit_bp = Blueprint('reddit_routes', __name__)
STATE = 'secure_random_state'

@reddit_bp.route('/')
def home():
    return '''
        <h1>Welcome to Reddit User Analysis</h1>
        <a href="/reddit/login">Login with Reddit</a>
    '''

@reddit_bp.route('/login')
def login():
    return get_auth_url()

@reddit_bp.route('/callback')
def callback():
    code = request.args.get('code')
    received_state = request.args.get('state')
    if received_state != STATE:
        return "State mismatch. Possible CSRF attack.", 400

    token_response = fetch_token(code)
    if token_response.status_code != 200:
        return f"Error fetching token: {token_response.text}", token_response.status_code

    session['access_token'] = token_response.json().get('access_token')
    return redirect(url_for('reddit_routes.analyze'))

@reddit_bp.route('/analyze')
def analyze():
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({"error": "User not logged in"}), 401

    user_response = fetch_user_profile(access_token)
    if user_response.status_code != 200:
        return jsonify({"error": f"Error fetching user profile: {user_response.text}"}), user_response.status_code

    user_data = user_response.json()
    username = user_data.get('name')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_row = cursor.fetchone()
    if user_row is None:
        return jsonify({"error": "User not found in the database"}), 404
    user_id = user_row['id']

    activity_responses = fetch_user_activity(username, access_token)
    overview_data = activity_responses['overview']
    upvoted_data = activity_responses['upvoted']
    downvoted_data = activity_responses['downvoted']

    posts = []
    comments = []
    upvoted = []
    downvoted = []
    sentiment_scores = []

    for item in overview_data.get('data', {}).get('children', []):
        if item.get('kind') == 't3':  # Post
            post_data = item['data']
            sentiment_score = analyze_sentiment(post_data.get('title', ''))
            post_data['sentiment_score'] = sentiment_score
            posts.append(post_data)
            sentiment_scores.append(sentiment_score)
            cursor.execute('INSERT INTO posts (user_id, title, sentiment_score) VALUES (?, ?, ?)',
                           (user_id, post_data.get('title', ''), sentiment_score))
        elif item.get('kind') == 't1':  # Comment
            comment_data = item['data']
            sentiment_score = analyze_sentiment(comment_data.get('body', ''))
            comment_data['sentiment_score'] = sentiment_score
            comments.append(comment_data)
            sentiment_scores.append(sentiment_score)
            cursor.execute('INSERT INTO comments (user_id, body, sentiment_score) VALUES (?, ?, ?)',
                           (user_id, comment_data.get('body', ''), sentiment_score))

    for item in upvoted_data.get('data', {}).get('children', []):
        if 'kind' in item:
            item_data = item['data']
            item_data['vote'] = 'upvoted'
            upvoted.append(item_data)

    for item in downvoted_data.get('data', {}).get('children', []):
        if 'kind' in item:
            item_data = item['data']
            item_data['vote'] = 'downvoted'
            downvoted.append(item_data)

    db.commit()
    db.close()

    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    top_subreddits = {}
    for post in posts + comments:
        subreddit = post.get('subreddit')
        if subreddit:
            top_subreddits[subreddit] = top_subreddits.get(subreddit, 0) + 1

    top_subreddits = sorted(top_subreddits.items(), key=lambda x: x[1], reverse=True)[:5]

    response_data = {
        "username": username,
        "number_of_posts": len(posts),
        "number_of_comments": len(comments),
        "average_sentiment": avg_sentiment,
        "top_subreddits": [{"subreddit": s[0], "activities": s[1]} for s in top_subreddits],
        "posts": [{"title": post['title'], "sentiment_score": post['sentiment_score']} for post in posts],
        "comments": [{"body": comment['body'], "sentiment_score": comment['sentiment_score']} for comment in comments],
        "upvoted": [{"title": item.get('title', ''), "body": item.get('body', ''), "vote": item['vote']} for item in upvoted],
        "downvoted": [{"title": item.get('title', ''), "body": item.get('body', ''), "vote": item['vote']} for item in downvoted]
    }

    return jsonify(response_data)
