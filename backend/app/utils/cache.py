import functools
import hashlib
import json
from typing import Any, Callable
import asyncio


def cache(ttl: int = 3600):
    """
    Simple in-memory cache decorator.
    In production, this should use Redis.
    """
    cache_data = {}

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_data = {
                "func": func.__name__,
                "args": str(args),
                "kwargs": str(sorted(kwargs.items())),
            }
            cache_key = hashlib.md5(json.dumps(key_data).encode()).hexdigest()

            # Check if cached
            if cache_key in cache_data:
                cached_value, cached_time = cache_data[cache_key]
                import time

                if time.time() - cached_time < ttl:
                    return cached_value

            # Call function and cache result
            result = await func(*args, **kwargs)
            import time

            cache_data[cache_key] = (result, time.time())
            return result

        return wrapper

    return decorator
