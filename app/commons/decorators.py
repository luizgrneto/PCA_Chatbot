import time
from functools import wraps

from app.commons.core import logger


def log_execution_time(func):
    """Decorator to log the execution time of async functions."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        func_name = func.__name__
        logger.info(f"Starting execution of {func_name}")

        try:
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                f"{func_name} completed successfully in {execution_time:.2f} seconds"
            )
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"{func_name} failed after {execution_time:.2f} seconds: {e}")
            raise

    return wrapper
