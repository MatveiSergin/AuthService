from fastapi import APIRouter, Depends
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
    print(user, data)
    print(user.role)
    role: RolesORM = user.role
    success: bool = await RolesCRUD.check_permissions(role, data)
    return ResponseCheck(success=success)