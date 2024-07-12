from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from cache import cache
from config_log import logger
from crud.base_crud import BaseCRUD, T, QueryValidator
from database.database import db_session
from models.models import RolesORM, PermissionsORM
from schemas.schemas import RoleBase, PermissionBase, RequestAccess


class RolesCRUD(BaseCRUD):
    orm_model = RolesORM
    schemas_model = RoleBase

    @classmethod
    async def get_all(cls, offset: int, limit: int) -> list[RoleBase]:
        logger.info(f"start crud function 'get_all' for orm_model {cls.orm_model} & offset={offset}; limit={limit} ")
        QueryValidator.validate_offset_and_limit(offset=offset, limit=limit)
        cache_data = await cache.get(f'get_all_{cls.orm_model} (offset={offset}; limit={limit})')

        if cache_data is not None:
            return cache_data

        async with db_session() as session:
            query = select(cls.orm_model)
            result = await session.execute(query)
            orm_objects = result.scalars().all()
            schemas_objects = list()
            for orm_object in orm_objects:
                permissions = [PermissionBase.from_orm(p) for p in orm_object.permissions]
                schemas_object = RoleBase.from_orm(orm_object).copy(update={"permissions": permissions})
                schemas_objects.append(schemas_object)

            await cache.set(f'get_all_{cls.orm_model} (offset={offset}; limit={limit})', repr(schemas_objects).encode())
            return schemas_objects

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[RoleBase]:
        logger.info(f"start crud function 'get_by_id' for orm_model {cls.orm_model} & id={id}")
        cache_data = await cache.get(f'get_by_id_{cls.orm_model} (id={id})')

        if cache_data is not None:
            return cache_data
        async with db_session() as session:
            orm_object = await session.get(cls.orm_model, id)
            if orm_object is not None:
                permissions = [PermissionBase.from_orm(p) for p in orm_object.permissions]
                schemas_object = RoleBase.from_orm(orm_object).copy(update={"permissions": permissions})
                await cache.set(f'get_by_id_{cls.orm_model} (id={id})', repr(schemas_object).encode())
                return schemas_object

    @classmethod
    async def check_permissions(cls, role: RolesORM, data: RequestAccess) -> bool:
        path = data.path
        method = data.method
        for permission in role.permissions:
            if permission.path == path and permission.method == method:
                return True
        return False

