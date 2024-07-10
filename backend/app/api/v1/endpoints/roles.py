from fastapi import APIRouter
from crud.roles import RolesCRUD
from schemas.schemas import RoleBase, ResponseSchemas, RoleAdd
from utils.decorators import log_data

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/all")
@log_data
async def get_roles() -> list[RoleBase]:
    roles = await RolesCRUD.get_all()
    return roles


@router.post("/add")
@log_data
async def add_role(role: RoleAdd) -> ResponseSchemas:
    id: int = await RolesCRUD.add_one(role)
    return ResponseSchemas(id=id)


@router.get("/{role_id}")
@log_data
async def get_role(id: int) -> RoleBase:
    role = await RolesCRUD.get_by_id(id)
    return role

@router.delete("/{role_id}")
@log_data
async def delete_role(id: int) -> ResponseSchemas:
    await RolesCRUD.delete_one(id)
    return ResponseSchemas(id=id)