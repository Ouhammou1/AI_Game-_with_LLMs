








from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ===========================
#  Chat Sessions Table
# ===========================
class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    session_id    = db.Column(db.String, primary_key=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    message_count = db.Column(db.Integer, default=0)

    # Relationship with the messages table
    messages = db.relationship('Message', backref='session', lazy=True)




# ===========================
#  Messages Table
# ===========================
class Message(db.Model):
    __tablename__ = 'messages'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String, db.ForeignKey('chat_sessions.session_id'), nullable=False)
    role       = db.Column(db.String, nullable=False)   # 'user' or 'assistant'
    content    = db.Column(db.Text, nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)


# ===========================
#  Save a new message
# ===========================
def save_message(session_id, role, content):
    try:
        # Find the session — create it if it doesn't exist
        session = ChatSession.query.get(session_id)
        if not session:
            session = ChatSession(session_id=session_id)
            db.session.add(session)

        # Add the new message
        msg = Message(session_id=session_id, role=role, content=content)
        db.session.add(msg)

        # Increment message counter
        session.message_count += 1
        session.updated_at = datetime.utcnow()

        db.session.commit()   # Save everything ✅

    except Exception as e:
        db.session.rollback() # Undo everything if an error occurs ✅
        print(f"[DB ERROR] Failed to save message: {e}")


# ===========================
#  Get all messages of a session
# ===========================
def get_messages(session_id):
    try:
        messages = (
            Message.query
            .filter_by(session_id=session_id)
            .order_by(Message.timestamp.asc())
            .all()
        )
        # Return as list of dicts — compatible with routes.py
        return [
            {
                "role":      m.role,
                "content":   m.content,
                "timestamp": m.timestamp  # datetime object, not string
            }
            for m in messages
        ]

    except Exception as e:
        print(f"[DB ERROR] Failed to get messages: {e}")
        return []


# ===========================
#  Get all chat sessions
# ===========================
def get_sessions():
    try:
        sessions = (
            ChatSession.query
            .order_by(ChatSession.updated_at.desc())
            .all()
        )

        result = []
        for s in sessions:
            # Get the first user message in this session
            first_msg = (
                Message.query
                .filter_by(session_id=s.session_id, role='user')
                .order_by(Message.timestamp.asc())
                .first()
            )

            # Title: first 30 characters of the first message
            if first_msg and len(first_msg.content) > 30:
                title = first_msg.content[:30] + '...'
            elif first_msg:
                title = first_msg.content
            else:
                title = 'New Chat'

            result.append({
                'session_id':    s.session_id,
                'title':         title,
                'message_count': s.message_count,
                'created_at':    s.created_at.isoformat()
            })

        return result

    except Exception as e:
        print(f"[DB ERROR] Failed to get sessions: {e}")
        return []