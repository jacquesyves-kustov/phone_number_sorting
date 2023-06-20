from functools import wraps
from time import perf_counter, process_time


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        start_process_time = process_time()

        # Do your magic!
        result = func(*args, **kwargs)

        end_process_time = process_time()
        end_time = perf_counter()

        print(f'Total time: {end_time - start_time}')
        print(f'Total process time: {end_process_time - start_process_time}')

        return result

    return wrapper
