from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_from_directory,
    Response,
    stream_with_context
)

from flask_cors import CORS
from datetime import datetime
import os
import re
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from LLM.chains import ask_llm, ask_llm_stream, reset_chat
from LLM.image_generator import generate_image


app = Flask(__name__)
CORS(app)

chat_history = []
SESSION_ID = str(uuid.uuid4())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        port=os.environ.get('DB_PORT', '5432'),
        dbname=os.environ.get('DB_NAME', 'chatbot_db'),
        user=os.environ.get('DB_USER', 'BRAHIM'),
        password=os.environ.get('DB_PASSWORD', '0000')
    )


def save_message(session_id, role, content):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO chat_sessions (session_id)
               VALUES (%s)
               ON CONFLICT (session_id) DO UPDATE
               SET message_count = chat_sessions.message_count + 1,
                   updated_at = CURRENT_TIMESTAMP""",
            (session_id,)
        )
        cur.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)",
            (session_id, role, content)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] Failed to save message: {e}")


def get_messages(session_id):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM messages WHERE session_id = %s ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB ERROR] Failed to get messages: {e}")
        return []


def format_response(response):
    response = re.sub(r'\*+', '', response)
    response = response.replace('\n', '<br>')
    return response


# =====================
# Static file routes
# =====================

@app.route('/q_table.json')
def serve_qtable():
    try:
        return send_from_directory(BASE_DIR, 'q_table.json')
    except Exception as e:
        print(f"Error serving q_table.json: {e}")
        return jsonify({'error': 'q_table.json not found'}), 404


@app.route('/static/q_table.json')
def serve_qtable_static():
    try:
        return send_from_directory(os.path.join(BASE_DIR, 'static'), 'q_table.json')
    except Exception:
        return jsonify({'error': 'q_table.json not found in static'}), 404


# =====================
# Page routes (HTML)
# =====================

@app.route('/')
def home():
    return redirect(url_for('game'))


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    global chat_history, SESSION_ID

    if request.method == 'POST':
        action = request.form.get('action', 'chat')
        user_message = request.form.get('message', '').strip()

        if action == "clear":
            chat_history.clear()
            SESSION_ID = str(uuid.uuid4())
            reset_chat()
            return render_template('chatbot.html', messages=chat_history)

        if action == "image":
            if user_message:
                result = generate_image(user_message)
                chat_history.append({'role': 'user', 'content': user_message, 'time': datetime.now().strftime('%H:%M')})
                save_message(SESSION_ID, 'user', user_message)
                if result.startswith("/static/"):
                    content = f"<img src='{result}' width='350' style='border-radius:8px;'>"
                else:
                    content = result
                chat_history.append({'role': 'bot', 'content': content, 'time': datetime.now().strftime('%H:%M')})
                save_message(SESSION_ID, 'bot', content)
            return render_template('chatbot.html', messages=chat_history)

        if user_message:
            image_keywords = ["generate image", "create image", "draw", "make image", "generate a photo", "create a photo", "imagine", "visualize", "generate for me image", "show me image", "show image", "generate me", "create me", "make me", "image of", "picture of", "photo of"]
            is_image_request = any(kw in user_message.lower() for kw in image_keywords)

            if is_image_request:
                clean_prompt = user_message.lower()
                for kw in image_keywords:
                    clean_prompt = clean_prompt.replace(kw, "").strip()
                clean_prompt = clean_prompt or user_message
                chat_history.append({'role': 'user', 'content': user_message, 'time': datetime.now().strftime('%H:%M')})
                save_message(SESSION_ID, 'user', user_message)
                result = generate_image(clean_prompt)
                if result.startswith("/static/"):
                    content = f"<img src='{result}' width='350' style='border-radius:8px;'>"
                else:
                    content = result
                chat_history.append({'role': 'bot', 'content': content, 'time': datetime.now().strftime('%H:%M')})
                save_message(SESSION_ID, 'bot', content)
            else:
                chat_history.append({'role': 'user', 'content': user_message, 'time': datetime.now().strftime('%H:%M')})
                save_message(SESSION_ID, 'user', user_message)
                try:
                    response = ask_llm(user_message)
                    response = format_response(response)
                except Exception as e:
                    response = f"Error: {str(e)}"
                chat_history.append({'role': 'bot', 'content': response, 'time': datetime.now().strftime('%H:%M')})
                save_message(SESSION_ID, 'bot', response)

        return render_template('chatbot.html', messages=chat_history)

    return render_template('chatbot.html', messages=chat_history)


# =====================
# JSON API routes
# =====================

@app.route('/api/chat', methods=['POST'])
def api_chat():
    global chat_history, SESSION_ID

    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    chat_history.append({'role': 'user', 'content': user_message, 'time': datetime.now().strftime('%H:%M')})
    save_message(SESSION_ID, 'user', user_message)

    image_keywords = ["generate image", "create image", "draw", "make image", "imagine", "visualize", "image of", "picture of", "photo of"]
    is_image_request = any(kw in user_message.lower() for kw in image_keywords)

    if is_image_request:
        clean_prompt = user_message.lower()
        for kw in image_keywords:
            clean_prompt = clean_prompt.replace(kw, "").strip()
        clean_prompt = clean_prompt or user_message
        result = generate_image(clean_prompt)
        if result.startswith("/static/"):
            content = f'<img src="{result}" width="350" style="border-radius:8px;">'
        else:
            content = result
    else:
        try:
            content = ask_llm(user_message)
            content = format_response(content)
        except Exception as e:
            content = f"Error: {str(e)}"

    chat_history.append({'role': 'bot', 'content': content, 'time': datetime.now().strftime('%H:%M')})
    save_message(SESSION_ID, 'bot', content)

    return jsonify({'role': 'bot', 'content': content, 'time': datetime.now().strftime('%H:%M')})


# =====================
# NEW: Streaming endpoint
# =====================

@app.route('/api/chat/stream', methods=['POST'])
def api_chat_stream():
    global chat_history, SESSION_ID

    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    chat_history.append({'role': 'user', 'content': user_message, 'time': datetime.now().strftime('%H:%M')})
    save_message(SESSION_ID, 'user', user_message)

    def generate():
        full_response = ''
        try:
            for token in ask_llm_stream(user_message):
                full_response += token
                yield f'data: {token}\n\n'
            yield 'data: [DONE]\n\n'
        except Exception as e:
            yield f'data: Error: {str(e)}\n\n'
            yield 'data: [DONE]\n\n'
            full_response = f'Error: {str(e)}'

        chat_history.append({'role': 'bot', 'content': full_response, 'time': datetime.now().strftime('%H:%M')})
        save_message(SESSION_ID, 'bot', full_response)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/api/clear', methods=['POST'])
def api_clear():
    global chat_history, SESSION_ID
    chat_history.clear()
    SESSION_ID = str(uuid.uuid4())
    reset_chat()
    return jsonify({'status': 'cleared'})


@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(chat_history)


@app.route('/api/new-session', methods=['POST'])
def api_new_session():
    global chat_history, SESSION_ID
    chat_history.clear()
    SESSION_ID = str(uuid.uuid4())
    reset_chat()
    return jsonify({'session_id': SESSION_ID})


@app.route('/api/set-session', methods=['POST'])
def api_set_session():
    global chat_history, SESSION_ID
    data = request.get_json()
    SESSION_ID = data.get('session_id', SESSION_ID)
    rows = get_messages(SESSION_ID)
    chat_history.clear()
    for row in rows:
        chat_history.append({
            'role': row['role'],
            'content': row['content'],
            'time': row['timestamp'].strftime('%H:%M') if row.get('timestamp') else ''
        })
    return jsonify({'messages': chat_history})


@app.route('/api/sessions', methods=['GET'])
def api_sessions():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT s.session_id, s.created_at, s.message_count,
                   (SELECT content FROM messages m
                    WHERE m.session_id = s.session_id AND m.role = 'user'
                    ORDER BY m.timestamp ASC LIMIT 1) as first_message
            FROM chat_sessions s
            ORDER BY s.updated_at DESC
        """)
        sessions = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for s in sessions:
            title = s['first_message'][:30] + '...' if s['first_message'] and len(s['first_message']) > 30 else (s['first_message'] or 'New Chat')
            result.append({
                'session_id': s['session_id'],
                'title': title,
                'message_count': s['message_count'],
                'created_at': s['created_at'].isoformat()
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================
# Serve React frontend
# =====================

@app.route('/studio')
def studio():
    return send_from_directory('static/llm-studio', 'index.html')


@app.route('/studio/<path:path>')
def studio_files(path):
    return send_from_directory('static/llm-studio', path)


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save with unique name
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({
        'filename': file.filename,
        'path': f'/static/uploads/{filename}',
        'size': os.path.getsize(filepath)
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)