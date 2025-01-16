import requests
from flask import redirect, request, url_for, session
from textblob import TextBlob

# Reddit app credentials (replace CLIENT_ID with your actual values)
CLIENT_ID = 'l8YUAHkHjkk2kPrfPFIh-w'
REDIRECT_URI = 'http://127.0.0.1:5000/reddit/callback'  # Ensure this matches the registered URI
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
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': USER_AGENT
    }
    response = requests.get(f"{API_BASE_URL}/user/{username}/overview", headers=headers)
    print(f"User activity response: {response.status_code} - {response.text}")
    return response

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity