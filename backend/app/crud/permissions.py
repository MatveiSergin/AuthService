from crud.base_crud import BaseCRUD
from models.models import PermissionsORM, RolesORM
from schemas.schemas import PermissionBase
from database.database import db_session

class PermissionsCRUD(BaseCRUD):
    orm_model = PermissionsORM
    schemas_model = PermissionBase

    @classmethod
    async def set_permission_to_role(cls, permission_id: int, role_id: int) -> None:
        async with db_session() as session:
            permission_orm = await session.get(PermissionsORM, permission_id)
            role_orm = await session.get(RolesORM, role_id)
            role_orm.permissions.append(permission_orm)
            await session.commit()

    @classmethod
    async def unset_permission_from_role(cls, permission_id: int, role_id: int) -> None:
        async with db_session() as session:
            role_orm = await session.get(RolesORM, role_id)
            for permission in role_orm.permissions:
                if permission.id == permission_id:
                    role_orm.permissions.remove(permission)
                    break
            await session.commit()