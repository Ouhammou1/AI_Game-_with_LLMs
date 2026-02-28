from langchain_core.messages import HumanMessage, AIMessage
from .llm_config import get_llm, get_system_message
from .rate_limiter import check_rate_limit
from .rate_limiter import set_processing
from .error_handler import handle_error
from .streaming import stream_response
from .timeout import run_with_timeout

llm = get_llm()
conversation_history = [get_system_message()]

print(conversation_history)


def ask_llm(message):
    try:
        check_rate_limit()
        set_processing(True)

        conversation_history.append(HumanMessage(content=message))

        response = run_with_timeout(
            llm.invoke,
            15,
            conversation_history
        )

        conversation_history.append(
            AIMessage(content=response.content)
        )

        return response.content

    except Exception as e:
        conversation_history.clear() #m
        return handle_error(e)
    
    finally:
        set_processing(False)



def ask_llm_stream(message):
    try:
        check_rate_limit()
        set_processing(True)
    except Exception as e:
        def error_gen():
            yield handle_error(e)
        return error_gen()

    return stream_response(llm, conversation_history, message)



def reset_chat():
    global conversation_history
    conversation_history = [get_system_message()]