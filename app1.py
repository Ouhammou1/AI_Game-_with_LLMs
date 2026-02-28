from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_from_directory
)
from flask_cors import CORS
from datetime import datetime
import os
import re
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from LLM.chains import ask_llm, reset_chat
from LLM.image_generator import generate_image

app = Flask(__name__)
CORS(app)

chat_history = []
SESSION_ID = str(uuid.uuid4())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==========================================
# Database
# ==========================================

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

        # Create session if not exists, else update count
        cur.execute(
            """INSERT INTO chat_sessions (session_id)
               VALUES (%s)
               ON CONFLICT (session_id) DO UPDATE
               SET message_count = chat_sessions.message_count + 1,
                   updated_at = CURRENT_TIMESTAMP""",
            (session_id,)
        )

        # Save the message
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


# ==========================================
# Serve Q-table
# ==========================================

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


# ==========================================
# Home
# ==========================================

@app.route('/')
def home():
    return redirect(url_for('game'))


# ==========================================
# Chatbot
# ==========================================

def format_response(response):
    response = re.sub(r'#{1,3}\s+(.+)', r'<strong>\1</strong>', response)
    response = re.sub(r'\*+', '', response)
    response = response.replace('\n', '<br>')
    return response


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    global chat_history, SESSION_ID

    if request.method == 'POST':

        action = request.form.get('action', 'chat')
        user_message = request.form.get('message', '').strip()

        # ==============================
        # CLEAR CHAT
        # ==============================
        if action == "clear":
            chat_history.clear()
            SESSION_ID = str(uuid.uuid4())  # new session on clear
            reset_chat()
            return render_template('chatbot.html', messages=chat_history)

        # ==============================
        # IMAGE GENERATION
        # ==============================
        if action == "image":
            if user_message:
                result = generate_image(user_message)

                chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'time': datetime.now().strftime('%H:%M')
                })
                save_message(SESSION_ID, 'user', user_message)

                if result.startswith("/static/"):
                    content = f"<img src='{result}' width='350' style='border-radius:8px;'>"
                else:
                    content = result

                chat_history.append({
                    'role': 'bot',
                    'content': content,
                    'time': datetime.now().strftime('%H:%M')
                })
                save_message(SESSION_ID, 'bot', content)

            return render_template('chatbot.html', messages=chat_history)

        # ==============================
        # NORMAL CHAT
        # ==============================
        if user_message:

            image_keywords = [
                "generate image", "create image", "draw", "make image",
                "generate a photo", "create a photo", "imagine", "visualize",
                "generate for me image", "show me image", "show image",
                "generate me", "create me", "make me", "image of",
                "picture of", "photo of"
            ]
            is_image_request = any(kw in user_message.lower() for kw in image_keywords)

            if is_image_request:
                clean_prompt = user_message.lower()
                for kw in image_keywords:
                    clean_prompt = clean_prompt.replace(kw, "").strip()
                clean_prompt = clean_prompt or user_message

                chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'time': datetime.now().strftime('%H:%M')
                })
                save_message(SESSION_ID, 'user', user_message)

                result = generate_image(clean_prompt)

                if result.startswith("/static/"):
                    content = f"<img src='{result}' width='350' style='border-radius:8px;'>"
                else:
                    content = result

                chat_history.append({
                    'role': 'bot',
                    'content': content,
                    'time': datetime.now().strftime('%H:%M')
                })
                save_message(SESSION_ID, 'bot', content)

            else:
                chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'time': datetime.now().strftime('%H:%M')
                })
                save_message(SESSION_ID, 'user', user_message)

                try:
                    response = ask_llm(user_message)
                    response = format_response(response)
                except Exception as e:
                    response = f"Error: {str(e)}"

                chat_history.append({
                    'role': 'bot',
                    'content': response,
                    'time': datetime.now().strftime('%H:%M')
                })
                save_message(SESSION_ID, 'bot', response)

        return render_template('chatbot.html', messages=chat_history)

    return render_template('chatbot.html', messages=chat_history)


# ==========================================
# Game Page
# ==========================================

@app.route('/game')
def game():
    return render_template('game.html')


# ==========================================
# Global Error Handler
# ==========================================

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


# ==========================================
# Run App
# ==========================================

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)