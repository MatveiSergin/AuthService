from database.database import db_session
from models.models import PermissionsORM, RolesORM

async def init_data():
    perm1 = PermissionsORM(method='GET', name='get_all_languages', path='/languages/all')
    perm2 = PermissionsORM(method='POST', name='add_language', path='/languages/add')
    perm3 = PermissionsORM(method='DELETE', name='delete_language', path='/languages')
    role1 = RolesORM(name='user', permissions=[perm1])
    role2 = RolesORM(name='admin', permissions=[perm1, perm2, perm3])
    async with db_session() as session:
        session.add_all([
            perm1,
            perm2,
            perm3,
            role1,
            role2,
        ])
        await session.commit()