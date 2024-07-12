from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends
from crud.roles import RolesCRUD
from schemas.schemas import RoleBase, ResponseSchemas, RoleAdd
from users import fastapi_users
from utils.decorators import log_data, is_admin

router = APIRouter(prefix="/roles", tags=["roles"])
current_user = fastapi_users.current_user()

@router.get("/all")
@log_data
@is_admin
async def get_roles(offset: int = 0, limit: int = 20, user=Depends(current_user)) -> list[RoleBase]:
    roles = await RolesCRUD.get_all(offset, limit)
    if roles is None:
        HTTPException(status_code=404, detail="Role does not exist")
    return roles


@router.post("/add")
@log_data
@is_admin
async def add_role(role: RoleAdd, user=Depends(current_user)) -> ResponseSchemas:
    id: int = await RolesCRUD.add_one(role)
    return ResponseSchemas(id=id)


@router.get("/{role_id}")
@log_data
@is_admin
async def get_role(id: int, user=Depends(current_user)) -> RoleBase:
    role = await RolesCRUD.get_by_id(id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role does not exist")
    return role

@router.delete("/{role_id}")
@log_data
@is_admin
async def delete_role(id: int, user=Depends(current_user)) -> ResponseSchemas:
    await RolesCRUD.delete_one(id)
    return ResponseSchemas(id=id)