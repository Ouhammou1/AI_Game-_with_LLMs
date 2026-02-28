import logging

logging.basicConfig(level=logging.INFO)

def handle_error(e):
    logging.error(f"LLM Error: {str(e)}")
    
    error_str = str(e).lower()
    if "timed out" in error_str:
        return "The AI is taking too long to respond. Please try again."
    elif "rate limit" in error_str:
        return "Too many requests. Please wait a moment and try again."
    elif "quota" in error_str or "exhausted" in error_str:
        return "API quota exceeded. Please try again later."
    else:
        return f"Error: {str(e)}"