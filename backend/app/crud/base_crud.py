from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
from database.database import db_session
from sqlalchemy import select, delete
from config_log import logger

T = TypeVar("T", bound=BaseModel)
ORMT = TypeVar("ORMT")

class BaseCRUD(Generic[T, ORMT]):
    orm_model = None
    schemas_model = None

    @classmethod
    async def add_one(cls, object: T) -> int:
        logger.info(f"start crud function 'add_one' for object {object} & orm_model {cls.orm_model}")
        async with db_session() as session:
            data: dict = object.model_dump()
            orm_obj = cls.orm_model(**data)
            session.add(orm_obj)
            await session.flush()
            await session.commit()
            logger.info(f"commit to db")
            return orm_obj.id

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[T]:
        logger.info(f"start crud function 'get_by_id' for orm_model {cls.orm_model} & id={id}")
        async with db_session() as session:
            orm_obj = await session.get(cls.orm_model, id)
            if orm_obj:
                schemas_obj = cls.schemas_model.model_validate(orm_obj.__dict__)
                return schemas_obj

    @classmethod
    async def get_all(cls) -> list[T]:
        logger.info(f"start crud function 'get_all' for orm_model {cls.orm_model}")
        async with db_session() as session:
            query = select(cls.orm_model)
            result = await session.execute(query)
            orm_objects = result.scalars().all()
            schemas_objects = [cls.schemas_model.model_validate(orm_object.__dict__) for orm_object in orm_objects]
            return schemas_objects

    @classmethod
    async def delete_one(cls, id: int) -> None:
        logger.info(f"start crud function 'delete_one' for orm_model {cls.orm_model} & id={id}")
        async with db_session() as session:
            query = delete(cls.orm_model).filter_by(id=id)
            await session.execute(query)
            await session.commit()
            logger.info(f"commit to db")

