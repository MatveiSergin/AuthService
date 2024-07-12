from fastapi import APIRouter, Depends
from crud.permissions import PermissionsCRUD
from models.models import UsersORM
from schemas.schemas import PermissionBase, ResponseSchemas, PermissionAdd
from users import fastapi_users
from utils.decorators import log_data, is_admin
from cache import cache
from fastapi.exceptions import HTTPException
router = APIRouter(prefix='/permissions', tags=["permissions"])

current_user = fastapi_users.current_user()

@router.get('/all')
@log_data
@is_admin
async def get_permissions(user: UsersORM = Depends(current_user), offset: int = 0, limit: int = 20) -> list[PermissionBase]:
    permissions = await PermissionsCRUD.get_all(offset, limit)
    return permissions

@router.get('/{permission_id}')
@log_data
@is_admin
async def get_permission(
        id: int,
        user: UsersORM = Depends(current_user)
        ) -> PermissionBase:
    permission = await PermissionsCRUD.get_by_id(id)
    if permission is None:
        HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.post('/add')
@log_data
@is_admin
async def add_permission(
        permission: PermissionAdd,
        user: UsersORM = Depends(current_user)
        ) -> ResponseSchemas:
    id: int = await PermissionsCRUD.add_one(permission)
    return ResponseSchemas(id=id)

@router.delete('/{permission_id}')
@log_data
@is_admin
async def delete_permission(
        id: int,
        user: UsersORM = Depends(current_user)
        ) -> ResponseSchemas:
    await PermissionsCRUD.delete_one(id)
    return ResponseSchemas(id=id)

@router.put('/set/{permission_id}/to/{role_id}')
@log_data
@is_admin
async def set_permission_to_role(
        permission_id: int,
        role_id: int,
        user: UsersORM = Depends(current_user)
        ) -> ResponseSchemas:
    await PermissionsCRUD.set_permission_to_role(permission_id, role_id)
    return ResponseSchemas()

@router.put('/unset/{permission_id}/from/{role_id}')
@log_data
@is_admin
async def delete_permission_from_role(
        permission_id: int,
        role_id: int,
        user: UsersORM = Depends(current_user)
        ) -> ResponseSchemas:
    await PermissionsCRUD.unset_permission_from_role(permission_id, role_id)
    return ResponseSchemas()
