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