from database.database import db_session
from database.utils import get_user_db
from models.models import PermissionsORM, RolesORM, UsersORM
from schemas.schemas import UserCreate
from users import UserManager
from settings.business_settings import business_settings

async def init_data():
    perm1 = PermissionsORM(method='GET', name='get_all_languages', path='/languages/all')
    perm2 = PermissionsORM(method='POST', name='add_language', path='/languages/add')
    perm3 = PermissionsORM(method='DELETE', name='delete_language', path='/languages')
    role1 = RolesORM(name='user', permissions=[perm1])
    role2 = RolesORM(name='admin', permissions=[perm1, perm2, perm3])

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
            perm1,
            perm2,
            perm3,
            role1,
            role2,
        ])
        await session.flush()
        create_admin = await UserManager(user_db).create(user_create=admin_schemas)
        #create_admin.role_id = business_settings.DEFAULT_ADMIN_ROLE_ID
        await session.commit()

