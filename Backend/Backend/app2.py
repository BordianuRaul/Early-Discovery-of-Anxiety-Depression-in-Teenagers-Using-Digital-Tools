from flask import Flask, redirect, request, url_for, session
import requests
from textblob import TextBlob
import time

# Flask app setup
app = Flask(__name__)
app.secret_key = 'secure_key_for_session'

# Reddit app credentials (replace CLIENT_ID with your actual values)
CLIENT_ID = 'l8YUAHkHjkk2kPrfPFIh-w'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
AUTH_BASE_URL = 'https://www.reddit.com/api/v1/authorize'
TOKEN_URL = 'https://www.reddit.com/api/v1/access_token'
API_BASE_URL = 'https://oauth.reddit.com'
USER_AGENT = 'Flask Reddit Analysis App'
STATE = 'secure_random_state'


@app.route('/')
def home():
    """
    Home page with a link to start Reddit OAuth.
    """
    return '''
        <h1>Welcome to Reddit User Analysis</h1>
        <a href="/login">Login with Reddit</a>
    '''


@app.route('/login')
def login():
    """
    Redirect the user to Reddit's OAuth2 authorization URL.
    """
    auth_url = (
        f"{AUTH_BASE_URL}"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&state={STATE}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&duration=temporary"
        f"&scope=identity history"
    )
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """
    Handle the OAuth2 callback and exchange the authorization code for an access token.
    """
    code = request.args.get('code')
    received_state = request.args.get('state')

    if received_state != STATE:
        return "State mismatch. Possible CSRF attack.", 400

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'User-Agent': USER_AGENT}
    token_response = requests.post(
        TOKEN_URL, data=data, headers=headers, auth=(CLIENT_ID, '')
    )

    if token_response.status_code != 200:
        return f"Error fetching token: {token_response.text}", token_response.status_code

    session['access_token'] = token_response.json().get('access_token')
    return redirect(url_for('analyze'))


@app.route('/analyze')
def analyze():
    """
    Fetch and analyze the authenticated user's Reddit activity with real-time updates.
    """
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT
    }

    # Fetch user profile
    user_response = requests.get(f"{API_BASE_URL}/api/v1/me", headers=headers)
    if user_response.status_code != 200:
        return f"Error fetching user profile: {user_response.text}", user_response.status_code

    user_data = user_response.json()
    username = user_data.get('name')

    # Fetch user activity (posts and comments)
    activity_response = requests.get(f"{API_BASE_URL}/user/{username}/overview", headers=headers)
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
            # Fetch upvotes and downvotes (polling for real-time updates)
            reactions_response = requests.get(f"{API_BASE_URL}/comments/{post_data['id']}", headers=headers)
            if reactions_response.status_code == 200:
                reactions_data = reactions_response.json()
                upvotes = reactions_data[0]['data']['children'][0]['data']['ups']
                downvotes = reactions_data[0]['data']['children'][0]['data']['downs']
            else:
                upvotes = 0
                downvotes = 0

            sentiment_score = TextBlob(post_data.get('title', '')).sentiment.polarity
            sentiment_scores.append(sentiment_score)

        elif item['kind'] == 't1':  # Comment
            comment_data = item['data']
            comments.append(comment_data)
            # Fetch upvotes and downvotes (polling for real-time updates)
            reactions_response = requests.get(f"{API_BASE_URL}/comments/{comment_data['link_id'][3:]}", headers=headers)
            if reactions_response.status_code == 200:
                reactions_data = reactions_response.json()
                upvotes = reactions_data[1]['data']['children'][0]['data']['ups']
                downvotes = reactions_data[1]['data']['children'][0]['data']['downs']
            else:
                upvotes = 0
                downvotes = 0

            sentiment_score = TextBlob(comment_data.get('body', '')).sentiment.polarity
            sentiment_scores.append(sentiment_score)

    # Calculate analysis results
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    top_subreddits = {}
    for post in posts + comments:
        subreddit = post.get('subreddit')
        if subreddit:
            top_subreddits[subreddit] = top_subreddits.get(subreddit, 0) + 1

    top_subreddits = sorted(top_subreddits.items(), key=lambda x: x[1], reverse=True)[:5]

    # Display results
    return f"""
        <h1>Analysis for {username}</h1>
        <p><b>Number of Posts:</b> {len(posts)}</p>
        <p><b>Number of Comments:</b> {len(comments)}</p>
        <p><b>Average Sentiment:</b> {avg_sentiment:.2f}</p>
        <p><b>Top Subreddits:</b> {', '.join([f"{s[0]} ({s[1]} activities)" for s in top_subreddits])}</p>
        <p><b>Upvotes:</b> {sum([r['ups'] for r in posts + comments])}</p>
        <p><b>Downvotes:</b> {sum([r['downs'] for r in posts + comments])}</p>
    """


if __name__ == '__main__':
    app.run(debug=True)
