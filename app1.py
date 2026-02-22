from flask import Flask  , request ,send_from_directory , jsonify , redirect , url_for , render_template
from flask_cors import CORS
import os
from datetime import datetime


app = Flask(__name__)
CORS(app)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chat_history = []



@app.route("/q_table.json")
def  serve_qtable():
    try:
        return send_from_directory(BASE_DIR , 'q_table1.json')
    except Exception as e:
        print(f"Error serving q_table.jon {e}")
        return jsonify(
            {'error': 'q_table not found'}
        ),404



@app.route('/')
def home():
    return redirect(url_for('game'))



@app.route('/chatbot' , methods=['GET' ,'POST'])
def  chatbot():
     if request.method == 'POST':
          user_message = request.form.get('message' , '')

          if user_message:
               chat_history.append(
                   {
                       'role' : 'user',
                       'content': user_message,
                       'time' : datetime.now().strftime('%H:%M')}
                       )
               # response  = ask_llm(user_message)

               chat_history.append(
                   {
                       'role' : 'bot',
                       'content': user_message,
                       'time' : datetime.now().strftime('%H:%M')}
                       )
               
          print(chat_history)
          return render_template('chatbot.html', messages=chat_history)
     return render_template('chatbot.html', messages=chat_history)



@app.route('/game')
def game():
     return render_template('game.html')

@app.route('/clear-chat')
def clear_chat():
    chat_history.clear()
    return redirect(url_for('chatbot'))

if __name__ == "__main__":
    app.run(debug=True, port=8000)

