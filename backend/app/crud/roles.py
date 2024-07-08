from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from crud.base_crud import BaseCRUD, T
from database.database import db_session
from models.models import RolesORM, PermissionsORM
from schemas.schemas import RoleBase, PermissionBase


class RolesCRUD(BaseCRUD):
    orm_model = RolesORM
    schemas_model = RoleBase

    @classmethod
    async def get_all(cls) -> list[RoleBase]:
        async with db_session() as session:
            query = select(cls.orm_model)
            result = await session.execute(query)
            orm_objects = result.scalars().all()
            schemas_objects = list()
            for orm_object in orm_objects:
                permissions = [PermissionBase.from_orm(p) for p in orm_object.permissions]
                schemas_object = RoleBase.from_orm(orm_object).copy(update={"permissions": permissions})
                schemas_objects.append(schemas_object)
            return schemas_objects

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[RoleBase]:
        async with db_session() as session:
            orm_object = await session.get(cls.orm_model, id)
            if orm_object:
                permissions = [PermissionBase.from_orm(p) for p in orm_object.permissions]
                schemas_object = RoleBase.from_orm(orm_object).copy(update={"permissions": permissions})
                return schemas_object