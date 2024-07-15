from sqlalchemy import update, select
from database.database import db_session
from database.utils import get_user_db
from models.models import PermissionsORM, RolesORM, UsersORM
from schemas.schemas import UserCreate
from users import UserManager
from settings.business_settings import business_settings
from fastapi import APIRouter

router = APIRouter(prefix="/init_data", tags=["init_data"])

@router.get("/")
async def init_data():
    perms = (
        PermissionsORM(method='GET', name='get_all_languages', path='/languages/all'),
        PermissionsORM(method='POST', name='add_language', path='/languages/add'),
        PermissionsORM(method='DELETE', name='delete_language', path='/languages'),
        PermissionsORM(method='GET', name='get_permissions', path='/permissions/all'),
    )
    roles = (
        RolesORM(name='user', permissions=[perms[0]]),
        RolesORM(name='admin', permissions=[perms[0], perms[1], perms[2]]),
    )

    user_gen = get_user_db()
    user_db = await anext(user_gen)
    admin_schemas = UserCreate(
        name=business_settings.ADMIN_ROLE,
        surname=business_settings.ADMIN_ROLE,
        role_id=business_settings.DEFAULT_ADMIN_ROLE_ID,
        email=f'{business_settings.ADMIN_ROLE}@{business_settings.ADMIN_ROLE}.{business_settings.ADMIN_ROLE}',
        password=business_settings.ADMIN_PASSWORD,
        is_active=True,
        is_superuser=True,
        is_verified=True
    )

    async with db_session() as session:
        session.add_all([
            *perms,
            *roles
        ])

        session.refresh(PermissionsORM)

        stmt = select(PermissionsORM, 1)
        res = await session.execute(stmt)
        data = res.all()
        if data:
            return

        await session.commit()

    await UserManager(user_db).create(user_create=admin_schemas)

    async with db_session() as session:
        stmt = update(UsersORM).filter_by(role_id=1).values(role_id=2)
        await session.execute(stmt)
        await session.commit()

    return {"data": "created"}
