<<<<<<< HEAD
<<<<<<< HEAD
from flask import Flask
from routes.mood_routes import mood_bp
from model.database import init_db

# Initialize Flask app
app = Flask(__name__)

# SQLite Database Configuration
app.config['DATABASE'] = 'instance/app.db'

# Initialize database
init_db(app)

# Register Blueprints
app.register_blueprint(mood_bp, url_prefix='/mood')

if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, request, redirect, url_for
import requests

app = Flask(__name__)

# Facebook App Details
APP_ID = '859918102701080'
APP_SECRET = '0621386803cd40f532d006b8dd50f34a'

def get_user_profile(access_token):
    # URL to fetch user profile info (you can modify this to get other data)
    url = 'https://graph.facebook.com/v12.0/me'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return response.json()

@app.route('/')
def home():
    # Constructing the OAuth URL for Facebook login
    facebook_oauth_url = (
        "https://www.facebook.com/v12.0/dialog/oauth?"
        "client_id={}&"
        "redirect_uri=https://127.0.0.1:8000/facebook/callback&"
        "scope=email,public_profile".format(APP_ID)  # Using valid permissions
    )
    return f'<a href="{facebook_oauth_url}">Log in with Facebook</a>'

@app.route('/facebook/callback')
def facebook_callback():
    # Step 1: Get the 'code' parameter from the redirect
    code = request.args.get('code')
    if code:
        # Step 2: Exchange the code for an access token
        token_url = "https://graph.facebook.com/v12.0/oauth/access_token"
        params = {
            'client_id': APP_ID,
            'redirect_uri': 'https://127.0.0.1:8000/facebook/callback',
            'client_secret': APP_SECRET,
            'code': code
        }
        token_response = requests.get(token_url, params=params)
        token_data = token_response.json()
        
        # Step 3: Check if access token is returned
        access_token = token_data.get('access_token')
        if access_token:
            user_profile = get_user_profile(access_token)
            user_name = user_profile.get('name', 'Unknown User')
            user_email = user_profile.get('email', 'Email not available')
            
            # Display the user information in a more friendly HTML format
            html_response = f"""
            <html>
                <head><title>Facebook Login Success</title></head>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px;">
                    <h1 style="color: #4CAF50;">Login Successful!</h1>
                    <p>Welcome, <strong>{user_name}</strong>!</p>
                    <p><strong>Email:</strong> {user_email}</p>
                    <h3>Profile Information:</h3>
                    <ul>
                        <li><strong>Full Name:</strong> {user_name}</li>
                        <li><strong>Email:</strong> {user_email}</li>
                    </ul>
                    <p><a href="/">Back to Home</a></p>
                </body>
            </html>
            """
            return html_response
        else:
            return "<p>Error: No access token received.</p>"
    
    return "<p>Error: No code received.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context=('sslcert.pem', 'sslkey.pem'))
>>>>>>> parent of 2d7f90f (AI model API; DB doesn't)
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from joblib import load
import os

# Extensions
db = SQLAlchemy()
jwt = JWTManager()

# Initialize the Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("reached here")

    # SQLite Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Create tables if they do not exist
    with app.app_context():
        db.create_all()
        print("db created")

    jwt.init_app(app)

    model_path = os.path.join(os.getcwd(), "AI_model",
                              "model_3_class_classifier_random_forests2.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    app.model = load(model_path)

    # from routes.auth_routes import auth_bp
    from routes.mood_routes import mood_bp

    # app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(mood_bp, url_prefix="/mood")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
>>>>>>> 2d7f90fe350b38b7d7f714a1bb23af6be6b7c538
