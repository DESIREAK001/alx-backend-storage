#!/usr/bin/env python3
"""
exercise.py
"""
from typing import Union, Optional, Callable, Any
import redis
import uuid
from functools import wraps


def replay(method: Callable) -> None:
    """
    Prints the history of calls to the function.

    Parameters:
        method: The function to print the hostory of.
    """
    name = method.__qualname__
    client = redis.Redis()
    inputs = client.lrange("{}:inputs".format(name), 0, -1)
    outputs = client.lrange("{}:outputs".format(name), 0, -1)
    print('{} was called {} times:'.format(name, len(inputs)))
    for input, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, input.decode("utf-8"),
                                     output.decode("utf-8")))


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a function is called.

    Parameters:
        fn: The function to be called.

    Returns:
        The decorated function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Increments the number of times the decorated function is called.

        Parameters:
            self: The instance of the Cache class.
            *args: The arguments to be passed to the decorated function.
            **kwargs: The keyword arguments to be passed to the decorated

        Returns:
            The return value of the decorated function.
        """
        if isinstance(self, Cache) and isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Returns the history of calls to the decorated function.

    Parameters:
        method: The function to be called.

    Returns:
        The decorated function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Returns the history of calls to the decorated function.

        Parameters:
            self: The instance of the Cache class.
            *args: The arguments to be passed to the decorated function.
            **kwargs: The keyword arguments to be passed to the decorated

        Returns:
            The return value of the decorated function.
        """
        input = "{}:inputs".format(method.__qualname__)
        output = "{}:outputs".format(method.__qualname__)
        return_value = method(self, *args, **kwargs)

        if isinstance(self, Cache) and isinstance(self._redis, redis.Redis):
            self._redis.rpush(input, str(args))
            self._redis.rpush(output, return_value)
        return return_value
    return wrapper


class Cache:
    """
    Cache class.

    This class is a wrapper around the Redis cache database.
    It provides a simple interface to store and retrieve data
    from the cache.
    """

    def __init__(self) -> None:
        """
        Initializes the cache class by creating a new Redis connection
        and removing any data in the db.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Saves the data in to the Redis db and returns
        the key to the value.

        Parameters:
            data: The data to be stored in the cache.

        Returns:
            The key to the value stored in the cache.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves the data associated with the key from the cache
        and returns it.

        Parameters:
            key: The key associated with the data in the cache.
            fn: A function that can be used to convert the data to
                the desired format. If provided, the data will be
                passed to the function. If not provided, the data
                will be returned as is.

        Returns:
            The data associated with the key in the cache. If a
            conversion function was provided, the converted data
            will be returned. Otherwise, the data will be returned
            as is.
        """
        data: bytes = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves the data associated with the key from the cache
        and returns it as a string.

        Parameters:
            key: The key associated with the data in the cache.

        Returns:
            The data associated with the key in the cache as a
            string.
        """
        value = self.get(key)
        if value is None:
            return None
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieves the data associated with the key from the cache
        and returns it as an integer.

        Parameters:
            key: The key associated with the data in the cache.

        Returns:
            The data associated with the key in the cache as an
            integer.
        """
        value = self.get(key)
        if value is None:
            return None
        return int(value)
