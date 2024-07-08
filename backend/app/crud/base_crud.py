from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
from database.database import db_session
from sqlalchemy import select, delete

from models.models import PermissionsORM
from schemas.schemas import PermissionBase, RoleBase

T = TypeVar("T", bound=BaseModel)
ORMT = TypeVar("ORMT")

class BaseCRUD(Generic[T, ORMT]):
    orm_model = None
    schemas_model = None

    @classmethod
    async def add_one(cls, object: T) -> int:
        async with db_session() as session:
            data: dict = object.model_dump()
            orm_obj = cls.orm_model(**data)
            session.add(orm_obj)
            await session.flush()
            await session.commit()
            return orm_obj.id

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[T]:
        async with db_session() as session:
            orm_obj = await session.get(cls.orm_model, id)
            if orm_obj:
                schemas_obj = cls.schemas_model.model_validate(orm_obj.__dict__)
                return schemas_obj

    @classmethod
    async def get_all(cls) -> list[T]:
        async with db_session() as session:
            query = select(cls.orm_model)
            result = await session.execute(query)
            orm_objects = result.scalars().all()
            schemas_objects = [cls.schemas_model.model_validate(orm_object.__dict__) for orm_object in orm_objects]
            return schemas_objects

    @classmethod
    async def delete_one(cls, id: int) -> None:
        async with db_session() as session:
            query = delete(cls.orm_model).filter_by(id=id)
            await session.execute(query)
            await session.commit()

