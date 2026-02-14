from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='.', template_folder='templates')
app.secret_key = 'game-secret-key'

# Store chat messages
chat_history = []

# ==================== ROUTES ====================

@app.route('/')
def serve_game():
    """Serve the main game page"""
    return send_from_directory('.', 'index.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    """Chatbot page"""
    global chat_history
    
    if request.method == 'POST':
        user_message = request.form.get('message', '')
        
        if user_message:
            # Add user message
            chat_history.append({
                'role': 'user',
                'content': user_message,
                'time': datetime.now().strftime('%H:%M')
            })
            
            # Get bot response
            bot_response = get_bot_response(user_message)
            
            # Add bot message
            chat_history.append({
                'role': 'bot',
                'content': bot_response,
                'time': datetime.now().strftime('%H:%M')
            })
    
    return render_template('chatbot.html', messages=chat_history)

@app.route('/clear-chat')
def clear_chat():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return redirect(url_for('chatbot'))

@app.route('/q_table.json')
def get_qtable():
    """Serve Q-table for game"""
    try:
        return send_from_directory('.', 'q_table.json')
    except:
        return jsonify({})

@app.route('/<path:path>')
def serve_files(path):
    """Serve all other files (script.js, style.css, etc.)"""
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

# ==================== RUN ====================

if __name__ == '__main__':
    print("="*50)
    print("🚀 Game server starting...")
    print("🎮 Play game: http://localhost:5000/")
    print("💬 Chatbot: http://localhost:5000/chatbot")
    print("="*50)
    app.run(debug=True, port=5000)