import functools
import time

from .exceptions import DomainException


def retry(exceptions, times=3):
    """
    Retries the function call N times when target exceptions occur.
    """
    max_time = 3  # max time sleep (is seconds)

    def wrapped(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            err = None
            sleep_time = 0
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    err = error
                    sleep_time += 1
                    time.sleep(min(sleep_time, max_time))
            else:
                raise DomainException('Service is busy. Try later.') from err

        return wrapper

    return wrapped
