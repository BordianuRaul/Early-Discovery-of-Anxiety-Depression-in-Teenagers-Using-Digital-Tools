# routes/auth_routes.py
from flask import Blueprint, request, jsonify, session, g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from model.database import get_db

auth_bp = Blueprint('auth_routes', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists.'}), 400

    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    session['user_id'] = user['id']
    return jsonify({'message': 'Logged in successfully.'}), 200