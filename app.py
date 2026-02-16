from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

try:
    from config import DATABASE_URL
except ImportError:
    # Fallback with GSSAPI disabled to fix macOS Kerberos issues
    DATABASE_URL = 'postgresql://BRAHIM:0000@localhost:5432/chatbot_db?sslmode=disable&gssencenc=disable'

app = Flask(__name__, static_folder='.', template_folder='templates')
app.secret_key = 'game-secret-key'

# ==================== DATABASE SETUP ====================

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class ChatMessage(db.Model):
    """Model representing a single chat message"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False, index=True)
    role = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'role': self.role,
            'content': self.content,
            'time': self.timestamp.strftime('%H:%M')
        }

class ChatSession(db.Model):
    """Model representing a conversation session"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    message_count = db.Column(db.Integer, default=0)

# ==================== ROUTES ====================

@app.route('/')
def serve_game():
    """Serve the main game page"""
    return send_from_directory('.', 'index.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    """Chatbot page - with PostgreSQL database storage"""
    session_id = request.args.get('session_id', f"session_{datetime.now().timestamp()}")
    
    if request.method == 'POST':
        user_message = request.form.get('message', '')
        
        if user_message:
            try:
                # Ensure session exists
                session = ChatSession.query.filter_by(session_id=session_id).first()
                if not session:
                    session = ChatSession(session_id=session_id)
                    db.session.add(session)
                    db.session.commit()
                
                # Store user message
                user_msg_record = ChatMessage(
                    session_id=session_id,
                    role='user',
                    content=user_message
                )
                db.session.add(user_msg_record)
                db.session.commit()
                
                # Get bot response
                bot_response = get_bot_response(user_message)
                
                # Store bot message
                bot_msg_record = ChatMessage(
                    session_id=session_id,
                    role='bot',
                    content=bot_response
                )
                db.session.add(bot_msg_record)
                
                # Update session
                session.message_count += 2
                session.updated_at = datetime.now()
                db.session.commit()
            except Exception as e:
                print(f"Error saving message: {e}")
                db.session.rollback()
    
    # Retrieve all messages for this session
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    
    return render_template('chatbot.html', messages=messages, session_id=session_id)

@app.route('/clear-chat')
def clear_chat():
    """Clear chat history for current session"""
    session_id = request.args.get('session_id')
    
    if session_id:
        try:
            ChatMessage.query.filter_by(session_id=session_id).delete()
            ChatSession.query.filter_by(session_id=session_id).delete()
            db.session.commit()
        except Exception as e:
            print(f"Error clearing chat: {e}")
            db.session.rollback()
    
    return redirect(url_for('chatbot'))

@app.route('/api/chat-history')
def get_chat_history():
    """API endpoint to retrieve chat history for a session"""
    session_id = request.args.get('session_id')
    
    if session_id:
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        return jsonify([msg.to_dict() for msg in messages])
    
    return jsonify([])

@app.route('/api/all-sessions')
def get_all_sessions():
    """API endpoint to retrieve all chat sessions"""
    try:
        sessions = ChatSession.query.order_by(ChatSession.updated_at.desc()).all()
        
        sessions_data = []
        for session in sessions:
            sessions_data.append({
                'session_id': session.session_id,
                'created_at': session.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': session.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'message_count': session.message_count
            })
        
        return jsonify(sessions_data)
    except Exception as e:
        print(f"Error retrieving sessions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/q_table.json')
def get_qtable():
    """Serve Q-table for game"""
    try:
        return send_from_directory('.', 'q_table.json')
    except:
        return jsonify({})

@app.route('/<path:path>')
def serve_files(path):
    """Serve all other files"""
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404

# ==================== BOT RESPONSES ====================

def get_bot_response(message):
    """Simple bot responses for Tic-Tac-Toe"""
    message = message.lower()
    
    responses = {
        'best move': "The best first move is the CENTER square! It gives you 4 winning lines.",
        'first move': "The best first move is the CENTER square! It gives you 4 winning lines.",
        'how to win': "Look for two of your marks in a row with an empty third space. Always block your opponent!",
        'strategy': "Control center, then corners. Block opponent's forks (where they can win two ways).",
        'tip': "Control center, then corners. Block opponent's forks (where they can win two ways).",
        'center': "Center is the most valuable square - it's part of 4 winning lines!",
        'corner': "Corners are good - each corner is part of 3 winning lines.",
        'edge': "Edges are weakest - only part of 2 winning lines. Avoid them as first move.",
        'q-learning': "Q-Learning is reinforcement learning where AI learns by trying moves and getting rewards. Our AI learned from 500,000 games!",
        'q learning': "Q-Learning is reinforcement learning where AI learns by trying moves and getting rewards. Our AI learned from 500,000 games!",
        'hello': "Hello! Ask me about Tic-Tac-Toe strategies!",
        'hi': "Hi there! Need help with your game?",
        'thanks': "You're welcome! Good luck with your game! 🎮",
        'thank you': "You're welcome! Good luck with your game! 🎮",
        'rule': "Rules: Players take turns placing X and O. First to get 3 in a row (horizontally, vertically, or diagonally) wins!",
        'rules': "Rules: Players take turns placing X and O. First to get 3 in a row (horizontally, vertically, or diagonally) wins!",
        'how play': "Click on any empty square to place X. The AI (O) will respond. First to get 3 in a row wins!"
    }
    
    for key in responses:
        if key in message:
            return responses[key]
    
    return f"Ask me about Tic-Tac-Toe! Try: 'best move', 'how to win', or 'strategy'."

# ==================== ERROR HANDLERS ====================

@app.errorhandler(Exception)
def handle_error(error):
    """Handle errors"""
    print(f"Error: {error}")
    return f"Error: {str(error)}", 500

# ==================== RUN ====================

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 SMART TIC-TAC-TOE - Game Server Starting")
    print("=" * 70)
    print("\n📍 Access Points:")
    print("   🎮 Game: http://localhost:5000/")
    print("   💬 Chatbot: http://localhost:5000/chatbot")
    print("   📊 API Sessions: http://localhost:5000/api/all-sessions")
    print("\n" + "=" * 70)
    
    # Create tables if needed
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database connection verified")
        except Exception as e:
            print(f"⚠️  Database warning: {e}")
    
    print("=" * 70 + "\n")
    app.run(debug=True, port=5000)