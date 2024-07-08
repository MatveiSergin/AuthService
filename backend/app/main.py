from contextlib import asynccontextmanager
import fastapi
from database.utils import create_tables
from database.initial_data import init_data
import uvicorn
from api.v1.routers import router as api_router
from models.models import PermissionsORM
from schemas.schemas import UserRead, UserCreate, UserUpdate, PermissionBase
from users import fastapi_users, auth_backend


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await create_tables()
    await init_data()
    yield


app = fastapi.FastAPI(
    lifespan=lifespan,
    title="AuthService")

app.include_router(api_router, prefix="/api/v1", tags=["ApiActions"])

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)