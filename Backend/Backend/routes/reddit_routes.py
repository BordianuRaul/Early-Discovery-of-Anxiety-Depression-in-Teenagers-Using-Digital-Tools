from flask import Blueprint, redirect, request, url_for, session, jsonify, current_app, g
from service.reddit_service import get_auth_url, fetch_token, fetch_user_profile, fetch_user_activity, analyze_sentiment
from service.model_AI import predict_sentiment
from model.models import User, Post, Comment
import sqlite3

reddit_bp = Blueprint('reddit_routes', __name__)
STATE = 'secure_random_state'

# helper to ease access to tht db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # Allows for dictionary-like access to rows
    return db

@reddit_bp.route('/')
def home():
    return '''
        <h1>Welcome to Reddit User Analysis</h1>
        <a href="/reddit/login">Login with Reddit</a>
    '''

@reddit_bp.route('/login')
def login():
    return redirect(get_auth_url())

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
        return redirect(url_for('reddit_routes.login'))

    user_response = fetch_user_profile(access_token)
    if user_response.status_code != 200:
        return f"Error fetching user profile: {user_response.text}", user_response.status_code

    user_data = user_response.json()
    username = user_data.get('name')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
    db.commit()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_id = cursor.fetchone()['id']

    activity_response = fetch_user_activity(username, access_token)
    if activity_response.status_code != 200:
        return f"Error fetching user activity: {activity_response.text}", activity_response.status_code

    activity_data = activity_response.json()
    posts = []
    comments = []
    sentiment_scores = []

    for item in activity_data.get('data', {}).get('children', []):
        if item['kind'] == 't3':  # Post
            post_data = item['data']
            posts.append(post_data)
            sentiment_score = analyze_sentiment(post_data.get('title', ''))
            sentiment_scores.append(sentiment_score)
            cursor.execute('INSERT INTO posts (user_id, title, sentiment_score) VALUES (?, ?, ?)',
                           (user_id, post_data.get('title', ''), sentiment_score))
        elif item['kind'] == 't1':  # Comment
            comment_data = item['data']
            comments.append(comment_data)
            sentiment_score = analyze_sentiment(comment_data.get('body', ''))
            sentiment_scores.append(sentiment_score)
            cursor.execute('INSERT INTO comments (user_id, body, sentiment_score) VALUES (?, ?, ?)',
                           (user_id, comment_data.get('body', ''), sentiment_score))

    db.commit()
    db.close()

    # predictions of the concatenated collected texts
    post_texts = [post['title'] for post in posts]
    comment_texts = [comment['body'] for comment in comments]
    all_texts = post_texts + comment_texts
    predictions = predict_sentiment(all_texts)

    # mapping the predictions of the model with the posts and comments
    post_predictions = predictions[:len(post_texts)]
    comment_predictions = predictions[len(post_texts):]

    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    top_subreddits = {}
    for post in posts + comments:
        subreddit = post.get('subreddit')
        if subreddit:
            top_subreddits[subreddit] = top_subreddits.get(subreddit, 0) + 1

    top_subreddits = sorted(top_subreddits.items(), key=lambda x: x[1], reverse=True)[:5]

    return f"""
        <h1>Analysis for {username}</h1>
        <p><b>Number of Posts:</b> {len(posts)}</p>
        <p><b>Number of Comments:</b> {len(comments)}</p>
        <p><b>Average Sentiment:</b> {avg_sentiment:.2f}</p>
        <p><b>Top Subreddits:</b> {', '.join([f"{s[0]} ({s[1]} activities)" for s in top_subreddits])}</p>
        <h2>Posts:</h2>
        <ul>
            {''.join([f"<li>{post['title']} - Sentiment: {post_predictions[i]}</li>" for i, post in enumerate(posts)])}
        </ul>
        <h2>Comments:</h2>
        <ul>
            {''.join([f"<li>{comment['body']} - Sentiment: {comment_predictions[i]}</li>" for i, comment in enumerate(comments)])}
        </ul>
    """