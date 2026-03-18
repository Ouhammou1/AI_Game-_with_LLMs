from flask import Flask
from database1 import db, ChatSession, Message
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    session_id = str(uuid.uuid4())

    s = ChatSession(session_id=session_id)
    db.session.add(s)

    m1 = Message(session_id=session_id, role="user", content="hello")
    m2 = Message(session_id=session_id, role="ai", content="hi!")

    db.session.add_all([m1, m2])
    db.session.commit()

    print(s.messages)