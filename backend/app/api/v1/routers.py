from fastapi import APIRouter
from api.v1.endpoints.roles import router as roles_router
from api.v1.endpoints.permissions import router as permission_router
from api.v1.endpoints.auth import router as auth_router


router = APIRouter()

router.include_router(roles_router)
router.include_router(permission_router)
router.include_router(auth_router)