from fastapi import APIRouter, Depends
from cache import cache
from crud.roles import RolesCRUD
from models.models import UsersORM, RolesORM
from schemas.schemas import RequestAccess, ResponseCheck
from users import fastapi_users
from utils.decorators import log_data
router = APIRouter(prefix='/auth', tags=["auth"])

current_user = fastapi_users.current_user()

@router.post("/check/access")
@log_data
async def check_access(data: RequestAccess, user: UsersORM = Depends(current_user)) -> ResponseCheck:
    role: RolesORM = user.role
    cache_success = await cache.get(f"check_access_for_{repr(data)}")
    if cache_success is not None:
        return ResponseCheck(success=cache_success)
    success: bool = await RolesCRUD.check_permissions(role, data)
    await cache.set(f"check_access_for_{repr(data)}", int(success))
    return ResponseCheck(success=success)