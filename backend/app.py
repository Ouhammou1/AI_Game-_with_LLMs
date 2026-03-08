from flask import Flask, request, jsonify, redirect, url_for, send_from_directory, render_template, Response, stream_with_context
from flask_cors import CORS
import os
import uuid

from database import Database
from routes import ChatManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize
db = Database()
chat = ChatManager(db)


# =====================
# Page routes
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

# @app.route('/static/q_table.json')
# def serve_qtable_static():
#     try:
#         return send_from_directory(os.path.join(BASE_DIR, 'static'), 'q_table.json')
#     except Exception:
#         return jsonify({'error': 'q_table.json not found in static'}), 404


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
    return jsonify(db.get_sessions())

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
# React frontend
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