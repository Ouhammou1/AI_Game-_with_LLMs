from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Store chat history in memory
chat_history = []

# Get the absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve q_table.json
@app.route('/q_table.json')
def serve_qtable():
    try:
        return send_from_directory(BASE_DIR, 'q_table.json')
    except Exception as e:
        return {'error': 'q_table.json not found'}, 404

# ===== CHATBOT ROUTES =====
@app.route('/')
def home():
    return redirect(url_for('game'))

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form.get('message', '')
        if user_message:
            chat_history.append({
                'role': 'user',
                'content': user_message,
                'time': datetime.now().strftime('%H:%M')
            })
            
            # Simple responses (not AI, just predefined)
            responses = {
                'minimax': 'To implement Minimax algorithm: evaluate all possible board states recursively, return scores for winning/losing positions, use alpha-beta pruning to optimize.',
                'tic': 'Tic-Tac-Toe is a perfect information game. The optimal strategy is to take the center, then corners.',
                'algorithm': 'Alpha-Beta pruning reduces the minimax search space by eliminating branches that cannot affect the final decision.',
                'optimization': 'To optimize game AI: memoize board states, reduce search depth, use heuristic evaluation functions.',
                'hello': 'Hello! How can I help with your game today?',
                'hi': 'Hi there! Ask me about game development!',
            }
            
            response = "I'm your game assistant! Ask me about minimax, algorithms, or Tic-Tac-Toe."
            for key, value in responses.items():
                if key in user_message.lower():
                    response = value
                    break
            
            chat_history.append({
                'role': 'bot',
                'content': response,
                'time': datetime.now().strftime('%H:%M')
            })
        
        return render_template('chatbot.html', messages=chat_history)
    
    return render_template('chatbot.html', messages=chat_history)

@app.route('/clear-chat')
def clear_chat():
    chat_history.clear()
    return redirect(url_for('chatbot'))

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)