from fastapi import APIRouter
from crud.permissions import PermissionsCRUD
from schemas.schemas import PermissionBase, ResponseSchemas
from utils.decorators import log_data

router = APIRouter(prefix='/permissions', tags=["permissions"])

@router.get('/all')
@log_data
async def get_permissions() -> list[PermissionBase]:
    permissions = await PermissionsCRUD.get_all()
    return permissions

@router.get('/{permission_id}')
@log_data
async def get_permission(id: int) -> PermissionBase:
    permission = await PermissionsCRUD.get_by_id(id)
    return permission

@router.post('/add')
@log_data
async def add_permission(permission: PermissionBase) -> ResponseSchemas:
    id: int = await PermissionsCRUD.add_one(permission)
    return ResponseSchemas(id=id)

@router.delete('/{permission_id}')
@log_data
async def delete_permission(id: int) -> ResponseSchemas:
    await PermissionsCRUD.delete_one(id)
    return ResponseSchemas(id=id)

@router.put('/set/{permission_id}/to/{role_id}')
@log_data
async def set_permission_to_role(permission_id: int, role_id: int) -> ResponseSchemas:
    await PermissionsCRUD.set_permission_to_role(permission_id, role_id)
    return ResponseSchemas()

@router.put('/unset/{permission_id}/from/{role_id}')
@log_data
async def delete_permission_from_role(permission_id: int, role_id: int) -> ResponseSchemas:
    await PermissionsCRUD.unset_permission_from_role(permission_id, role_id)
    return ResponseSchemas()
