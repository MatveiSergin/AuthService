import fastapi
from contextlib import asynccontextmanager
from database.initial_data import init_data
from database.utils import create_tables
from api.v1.routers import router as api_router
from schemas.schemas import UserRead, UserCreate, UserUpdate
from users import fastapi_users, auth_backend
from config_log import logger


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    logger.info("Starting lifespan context manager")
    await create_tables()
    await init_data()

    yield
    logger.info("Lifespan context manager complete")

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

@app.middleware("http")
async def log_requests(request: fastapi.Request, call_next):
    logger.info(f"[MIDDLEWARE] Request: {request.method} {request.url}")

    response = await call_next(request)
    logger.info(f"[MIDDLEWARE] Response: {response.status_code}")
    return response

@app.middleware("http")
async def check_access(request: fastapi.Request, call_next):
    response = await call_next(request)
    return response

