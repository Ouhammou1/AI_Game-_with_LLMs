from flask import Flask 
from flask_cors import CORS
import os
from dotenv import load_dotenv

from database import db, get_sessions, ChatSession, Message




load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR,  'templates'),
    static_folder=os.path.join(BASE_DIR  , 'static')
)
CORS(app)











UPLOAD_FOLDER = os.path.join(BASE_DIR , 'uploads')
os.makedirs(UPLOAD_FOLDER , exist_ok=True)


