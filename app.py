from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

from LLM.chains import ask_llm

app = Flask(__name__)
CORS(app)

chat_history = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    except:
        return jsonify({'error': 'q_table.json not found in static'}), 404

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

            try:
                response = ask_llm(user_message)
            except Exception as e:
                response = f"Error : {str(e)}"

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
    app.run(host="0.0.0.0", port=5000, debug=True)

