# import time
# from collections import deque

# REQUEST_LIMIT = 50
# TIME_WINDOW = 60  # seconds

# request_log = deque()

# def check_rate_limit():
#     current_time = time.time()

#     while request_log and current_time - request_log[0] > TIME_WINDOW:
#         request_log.popleft()

#     if len(request_log) >= REQUEST_LIMIT:
#         raise Exception("Rate limit exceeded. Please try again later.")

#     request_log.append(current_time)



# if __name__ == "__main__" :
#     check_rate_limit()
#     print(request_log)