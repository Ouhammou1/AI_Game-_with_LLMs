
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    streaming=True
)

conversation_history = [
    SystemMessage(content="You are a helpful assistant that answers clearly and concisely.")
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {topic}. Answer in {language}."),
    ("human", "{question}")
])
chain = prompt | llm


def ask_llm_simple(message: str) -> str:
    response = llm.invoke(message)
    return response.content


def ask_llm_with_system(message: str) -> str:
    messages = [
        SystemMessage(content="You are a helpful assistant that answers clearly and concisely."),
        HumanMessage(content=message)
    ]
    response = llm.invoke(messages)
    return response.content


def ask_llm(message: str) -> str:
    conversation_history.append(HumanMessage(content=message))
    response = llm.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content))
    return response.content


def ask_llm_template(question: str, topic="programming", language="English") -> str:
    response = chain.invoke({
        "topic": topic,
        "language": language,
        "question": question
    })
    return response.content

def ask_ll_stream(message: str):
    for chunk in llm.stream(message):
        yield chunk.content