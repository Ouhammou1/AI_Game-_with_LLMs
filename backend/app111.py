from flask import Flask, request, jsonify, redirect, url_for, send_from_directory, render_template, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
import json as _json
import random as _random
import time
from database import db, get_sessions #, ChatSession, Message
from routes import ChatManager

load_dotenv()  # Load .env file

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)

# ===========================
# Database Configuration
# ===========================
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/backend/database.db'


app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.environ.get('DB_USER')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}:"
    f"{os.environ.get('DB_PORT')}/"
    f"{os.environ.get('DB_NAME')}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 1800,
    'pool_pre_ping': True   # Auto-check connection before use
}

db.init_app(app)  # Link SQLAlchemy with Flask


# ===========================
# Wait for Database to be Ready
# ===========================
def init_db():
    retries = 5
    for i in range(retries):
        try:
            with app.app_context():
                db.create_all()
                print("✅ Database connected and tables created!")
                return
        except Exception as e:
            print(f"⏳ Waiting for database... attempt {i+1}/{retries}: {e}")
            time.sleep(3)
    print("❌ Could not connect to database after 5 attempts!")

init_db()


# ===========================
# Upload Folder
# ===========================
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize ChatManager
chat = ChatManager()


# =====================
# AI (Q-Table)
# =====================
Q_TABLE_PATH = os.path.join(BASE_DIR, 'q_table.json')
try:
    with open(Q_TABLE_PATH, 'r') as f:
        q_table = _json.load(f)
    print(f"Q-table loaded: {len(q_table)} states")
except FileNotFoundError:
    q_table = {}
    print("q_table.json not found")

# def _get_state(board, phase, player):
#     return ''.join([c if c else '-' for c in board]) + f"_{phase}_{player}"

# def _get_available_actions(board, phase, player):
#     if phase == 'place':
#         return [{'type': 'place', 'to': i, 'key': f'p{i}'}
#                 for i, c in enumerate(board) if c == '']
#     my_pieces = [i for i, c in enumerate(board) if c == player]
#     if len(my_pieces) < 3:
#         return []
#     empty     = [i for i, c in enumerate(board) if c == '']
#     return [{'type': 'move', 'from': frm, 'to': to, 'key': f'm{frm}_{to}'}
#             for frm in my_pieces for to in empty]

# def _get_best_action(state, actions):
#     if state not in q_table:
#         return _random.choice(actions)
#     return max(actions, key=lambda a: q_table[state].get(a['key'], 0.0))



def _get_state(board, phase, player):
    state = ""
    for cell in board:
        if cell == '':
            state += "-"
        else:
            state +=cell
    
    state += "_" + phase + "_" + player
    return state
    

def _get_available_actions(board, phase, player):
    actions =[]
    if phase == 'place':
        for i in range(len(board)):
            if board[i] == '':
                action = {
                    'type' : 'place',
                    'to' : i,
                    'key' : 'p' + str(i)
                }
                actions.append(action)
        return actions
    
    my_pieces =[]
    empty_cells= []

    for i in range(len(board)):
        if board[i] == player :
            my_pieces.append(i)
        elif board[i] == '':
            empty_cells.append(i)
    
    if len(my_pieces) < 3:
        return []

    for j in my_pieces:
        for k in empty_cells:
            action = {
                'type' : 'move',
                'from' : j,
                'to' : k ,
                'key': 'm' + str (j) + '_' + str(k)
            }
            actions.append(action)
    return actions



def _get_best_action(state, actions):
    if state not in q_table:
        return  _random.choice(actions)
    
    best_action = None
    best_value = float('-inf')
    print(f"best value {best_value}")

    for action in actions:
        key = action['key']
        value = q_table[state].get(key , 0.0)
        if value > best_value:
            best_value = value
            best_action = action
        
    return best_action




# =====================
# Page Routes
# =====================
@app.route('/')
def home():
    return redirect(url_for('game'))

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/q_table.json')
def serve_qtable():
    try:
        return send_from_directory(BASE_DIR, 'q_table.json')
    except Exception:
        return jsonify({'error': 'q_table.json not found'}), 404


# =====================
# AI API
# =====================
@app.route('/api/ai-move', methods=['POST'])
def api_ai_move():
    data   = request.get_json()
    board  = data.get('board')
    phase  = data.get('phase')
    player = data.get('player', 'O')

    if not board or not phase:
        return jsonify({'error': 'board and phase required'}), 400

    state     = _get_state(board, phase, player)
    available = _get_available_actions(board, phase, player)

    if not available:
        return jsonify({'error': 'no moves available'}), 400

    action = _get_best_action(state, available)
    return jsonify(action)


# =====================
# Chat API
# =====================
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    result = chat.chat(data.get('message', '').strip())
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)



@app.route('/api/chat/stream', methods=['POST'])
def api_chat_stream():
    data = request.get_json()
    message = data.get('message', '').strip()
    generator = chat.chat_stream(message)
    if not generator:
        return jsonify({'error': 'Empty message'}), 400
    return Response(
        stream_with_context(generator()),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
    )


# =====================
# Session API
# =====================

@app.route('/api/new-session', methods=['POST'])
def api_new_session():
    session_id = chat.new_session()
    return jsonify({'session_id': session_id})

@app.route('/api/set-session', methods=['POST'])
def api_set_session():
    data = request.get_json()
    messages = chat.set_session(data.get('session_id'))
    return jsonify({'messages': messages})

@app.route('/api/sessions', methods=['GET'])
def api_sessions():
    return jsonify(get_sessions())

@app.route('/api/clear', methods=['POST'])
def api_clear():
    chat.clear()
    return jsonify({'status': 'cleared'})

@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(chat.chat_history)


# =====================
# Upload API
# =====================
@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return jsonify({
        'filename': file.filename,
        'path': f'/static/uploads/{filename}',
        'size': os.path.getsize(filepath)
    })


# =====================
# React Frontend
# =====================
@app.route('/studio')
def studio():
    return send_from_directory(os.path.join(BASE_DIR, 'static', 'llm-studio'), 'index.html')

@app.route('/studio/<path:path>')
def studio_files(path):
    return send_from_directory(os.path.join(BASE_DIR, 'static', 'llm-studio'), path)


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)