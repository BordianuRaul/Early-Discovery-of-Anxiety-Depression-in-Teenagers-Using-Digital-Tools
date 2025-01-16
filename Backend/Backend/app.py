import os
from flask_cors import CORS
from flask import Flask, render_template
from routes.mood_routes import mood_bp
from routes.reddit_routes import reddit_bp
from routes.auth_routes import auth_bp
from routes.analysis_routes import analysis_bp
from model.database import init_db
from utils import utils

utils.load_env()
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

# SQLite Database Configuration
app.config['DATABASE'] = 'instance/app.db'

init_db(app)

app.register_blueprint(mood_bp, url_prefix='/mood')
app.register_blueprint(reddit_bp, url_prefix='/reddit')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(analysis_bp, url_prefix="/analysis")

@app.route('/')
def landing_page():
    return render_template("landing.html")

# main app
if __name__ == "__main__":
    app.run(debug=True)