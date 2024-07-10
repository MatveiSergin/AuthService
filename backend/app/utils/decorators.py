import functools
from config_log import logger

def log_data(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f'Start <{func.__name__}> with args {args}, kwargs {kwargs}')
        result = await func(*args, **kwargs)
        logger.info(f'End <{func.__name__}> with return: {result}')
        return result
    return wrapper