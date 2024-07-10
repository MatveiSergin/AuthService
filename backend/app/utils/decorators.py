import functools
from fastapi import status
from config_log import logger
from fastapi.exceptions import HTTPException
from models.models import UsersORM
from settings.business_settings import business_settings


def log_data(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f'Start <{func.__name__}> with args {args}, kwargs {kwargs}')
        result = await func(*args, **kwargs)
        logger.info(f'End <{func.__name__}> with return: {result}')
        return result
    return wrapper

def is_admin(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        user: UsersORM = kwargs.get('user', None)
        if not user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if user.role != business_settings.ADMIN_ROLE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await func(*args, **kwargs)

    return wrapper