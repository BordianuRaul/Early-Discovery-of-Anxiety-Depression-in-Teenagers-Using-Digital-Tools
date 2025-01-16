from flask import Blueprint, request, jsonify, g, current_app
import sqlite3


journal_bp = Blueprint('journal', __name__)

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # Allows for dictionary-like access to rows
        print("It gets in get db4")

    return db

@journal_bp.route('/addJournalDay', methods=['POST'])
def add_journal_day():
    data = request.get_json()

    userId = data['userId']
    content = data['content']
    print("ite gets here", data)
    db = get_db()

    cursor = db.cursor()

    try:
        cursor.execute('INSERT INTO journals (userId, content) VALUES (?, ?)', (userId, content))
        db.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()  # Ensure connection is closed

    return jsonify({'message': 'Journal day added successfully'}), 201
