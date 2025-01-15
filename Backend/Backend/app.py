import os
from flask import Flask, render_template
from routes.mood_routes import mood_bp
from routes.reddit_routes import reddit_bp
from model.database import init_db
from utils import utils

utils.load_env()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# SQLite Database Configuration
app.config['DATABASE'] = 'instance/app.db'

# Initialize database
init_db(app)

# Register Blueprints
app.register_blueprint(mood_bp, url_prefix='/mood')
app.register_blueprint(reddit_bp, url_prefix='/reddit')

@app.route('/')
def landing_page():
    return render_template("landing.html")

if __name__ == "__main__":
    app.run(debug=True)