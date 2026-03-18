from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    session_id    = db.Column(db.String, primary_key=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime , default=datetime.utcnow , onupdate=datetime.utcnow)
    message_count =  db.Column(db.Integer , default=0)

    messages = db.relationship('Message' , backref='session' , lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    session_id  = db.Column(db.String, db.ForeignKey('chat_sessions.session_id') , nullable=False)
    role = db.Column(db.String , nullable=False)
    content = db.Column(db.Text , nullable=False)
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)