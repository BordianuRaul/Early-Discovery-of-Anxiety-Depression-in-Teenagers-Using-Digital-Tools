import requests
from flask import redirect, request, url_for, session
from textblob import TextBlob

# Reddit app credentials (replace CLIENT_ID with your actual values)
CLIENT_ID = 'l8YUAHkHjkk2kPrfPFIh-w'
REDIRECT_URI = 'http://10.0.2.2:5000/reddit/callback'  # Ensure this matches the registered URI
AUTH_BASE_URL = 'https://www.reddit.com/api/v1/authorize'
TOKEN_URL = 'https://www.reddit.com/api/v1/access_token'
API_BASE_URL = 'https://oauth.reddit.com'
USER_AGENT = 'Flask Reddit Analysis App'
STATE = 'secure_random_state'

def get_auth_url():
    return (
        f"{AUTH_BASE_URL}"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&state={STATE}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&duration=temporary"
        f"&scope=identity history"
    )

def fetch_token(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'User-Agent': USER_AGENT}
    response = requests.post(TOKEN_URL, data=data, headers=headers, auth=(CLIENT_ID, ''))
    print(f"Token response: {response.status_code} - {response.text}")
    return response

def fetch_user_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT
    }
    response = requests.get(f"{API_BASE_URL}/api/v1/me", headers=headers)
    print(f"User profile response: {response.status_code} - {response.text}")
    return response

def fetch_user_activity(username, access_token):
    """
    Fetches the Reddit user's activity (overview, upvoted, downvoted).
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT
    }

    overview_response = requests.get(f"{API_BASE_URL}/user/{username}/overview", headers=headers)
    upvoted_response = requests.get(f"{API_BASE_URL}/user/{username}/upvoted", headers=headers)
    downvoted_response = requests.get(f"{API_BASE_URL}/user/{username}/downvoted", headers=headers)

    # Check response status and parse JSON
    if overview_response.status_code != 200:
        raise Exception(f"Error fetching overview: {overview_response.text}")
    if upvoted_response.status_code != 200:
        raise Exception(f"Error fetching upvoted: {upvoted_response.text}")
    if downvoted_response.status_code != 200:
        raise Exception(f"Error fetching downvoted: {downvoted_response.text}")

    return {
        'overview': overview_response.json(),  # Return parsed JSON
        'upvoted': upvoted_response.json(),   # Return parsed JSON
        'downvoted': downvoted_response.json()  # Return parsed JSON
    }

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity