import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        port=os.environ.get('DB_PORT', '5432'),
        dbname=os.environ.get('DB_NAME', 'chatbot_db'),
        user=os.environ.get('DB_USER', 'BRAHIM'),
        password=os.environ.get('DB_PASSWORD', '0000')
    )

def save_message(session_id, role, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)",
        (session_id, role, content)
    )
    cur.execute(
        """INSERT INTO chat_sessions (session_id) VALUES (%s)
           ON CONFLICT (session_id) DO UPDATE 
           SET message_count = chat_sessions.message_count + 1,
               updated_at = CURRENT_TIMESTAMP""",
        (session_id,)
    )
    conn.commit()
    cur.close()
    conn.close()