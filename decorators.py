import logging
from functools import wraps
from typing import Optional, Callable, Any


def log(filename: Optional[str] = None) -> Callable:
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format='%(message)s'
    )

    logger = logging.getLogger()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise e

        return wrapper

    return decorator
