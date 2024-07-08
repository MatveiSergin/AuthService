from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from settings import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.ENGINE_ECHO,
    pool_size=settings.ENGINE_POOL_SIZE,
)
class ModelORM(DeclarativeBase): pass

class User(SQLAlchemyBaseUserTableUUID, ModelORM):
    pass

db_session = async_sessionmaker(engine, expire_on_commit=False)
