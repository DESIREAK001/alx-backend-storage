#!/usr/bin/env python3
""" web.py """
import requests
from typing import Callable, Any
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a function is called.

    Parameters:
        fn: The function to be called.

    Returns:
        The decorated function.
    """

    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Increments the number of times the decorated function is called.

        Parameters:
            self: The instance of the Cache class.
            *args: The arguments to be passed to the decorated function.
            **kwargs: The keyword arguments to be passed to the decorated

        Returns:
            The return value of the decorated function.
        """
        clinet = redis.Redis()

        count_key = "count:{url}".format(url=url)
        result_key = "result:{url}".format(url=url)
        clinet.incr(count_key)

        result = clinet.get(result_key)
        if result:
            return result.decode("utf-8")

        return_value = method(url)
        clinet.setex(result_key, 10, return_value)

        return return_value
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Retrieves the content of a web page.

    Parameters:
        url: The URL of the web page to retrieve.

    Returns:
        The content of the web page.
    """
    try:
        return requests.get(url).text
    except requests.RequestException:
        return str(None)
