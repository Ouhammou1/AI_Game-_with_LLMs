import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

load_dotenv()

# def get_llm():
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         temperature=0.7,
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         streaming=True
#     )



# def get_llm():
#     return ChatGroq(
#         model="llama-3.3-70b-versatile",
#         temperature=0.7,
#         groq_api_key=os.getenv("GROQ_API_KEY"),
#         streaming=True
#     )




def get_llm():
    return ChatOpenAI(
        model="meta-llama/llama-3.3-70b-instruct",  # or any model from OpenRouter
        temperature=0.7,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        streaming=True,
        default_headers={
            "HTTP-Referer": "https://yourapp.com",  # optional but recommended
            "X-Title": "Your App Name",             # optional but recommended
        }
    )

def get_system_message():
    return SystemMessage(
        content=(
            "You are a helpful and knowledgeable AI assistant like ChatGPT. "
            "Always respond in the same language as the user's question. "
            "Give detailed, thorough answers with explanations and examples when helpful. "
            "Use clear structure: introduce the topic, explain it, give examples if needed. "
            "For lists use numbers like 1. 2. 3. or dashes - only. "
            "Do not use markdown formatting like ###, **, or ---. "
            "Use plain text only. "
            "If unsure, say you don't know. "
        )
    )