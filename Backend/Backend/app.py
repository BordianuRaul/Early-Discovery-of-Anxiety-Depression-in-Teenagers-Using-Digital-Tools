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
