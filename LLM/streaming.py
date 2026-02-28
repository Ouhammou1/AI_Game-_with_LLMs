from langchain_core.messages import HumanMessage, AIMessage
from .rate_limiter import set_processing
from .error_handler import handle_error

def stream_response(llm, conversation_history, message):
    try:
        conversation_history.append(HumanMessage(content=message))
        full_response = ""

        for chunk in llm.stream(conversation_history):
            if chunk.content:
                full_response += chunk.content
                yield chunk.content  

        conversation_history.append(AIMessage(content=full_response))

    except Exception as e:
        conversation_history.clear()
        yield handle_error(e)

    finally:
        set_processing(False)           