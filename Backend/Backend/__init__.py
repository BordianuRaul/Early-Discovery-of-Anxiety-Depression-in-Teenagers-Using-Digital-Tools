from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# Extensions used within the application
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    jwt.init_app(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.mood_routes import mood_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(mood_bp, url_prefix="/mood")

    return app