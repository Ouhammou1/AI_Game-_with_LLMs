from concurrent.futures import ThreadPoolExecutor, TimeoutError

class TimeoutException(Exception):
    pass

def run_with_timeout(func, seconds=15, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=seconds)
        except TimeoutError:
            raise TimeoutException("Request timed out.")

