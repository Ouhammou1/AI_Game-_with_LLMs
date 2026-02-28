import time

is_processing = False

def check_rate_limit():
    global is_processing
    if is_processing:
        raise Exception("Please wait... AI is still responding")

def set_processing(state: bool):
    global is_processing
    is_processing = state