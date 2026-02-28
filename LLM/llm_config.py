import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

from langchain_groq import ChatGroq

load_dotenv()

# def get_llm():
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         temperature=0.7,
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         streaming=True
#     )



def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        streaming=True
    )


def get_system_message():
    return SystemMessage(
        content=(
            "You are a professional AI assistant. "
            # "Answer clearly and accurately. "
            "Always respond in the same language as the user's question. "
            "If unsure, say you don't know. "
            "Keep answers concise and to the point. "
            "Do not use markdown formatting like ###, **, or ---. "
            "Use plain text only. "
            "For lists use numbers like 1. 2. 3. or dashes - only. "
            # "Do not add unnecessary explanations or extra details unless asked."
        )
    )