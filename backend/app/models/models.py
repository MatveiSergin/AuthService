from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum
from database.database import ModelORM

class Methods(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

class PermissionsORM(ModelORM):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(autoincrement='auto', primary_key=True)
    name: Mapped[str]
    #method = mapped_column(SQLAlchemyEnum(Methods), nullable=False)
    method: Mapped[str]
    path: Mapped[str]
    roles: Mapped[list["RolesORM"]] = relationship(back_populates='permissions', lazy='selectin', secondary='associations_roles_permissions', uselist=True)

    def __repr__(self):
        return f'<PermissionsORM: name: {self.name}; method: {self.method}; path: {self.path}'

class AssociationsRolesPermissions(ModelORM):
    __tablename__ = 'associations_roles_permissions'
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permissions_id: Mapped[int] = mapped_column(ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)

class RolesORM(ModelORM):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(autoincrement='auto', primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    permissions: Mapped[list["PermissionsORM"]] = relationship(back_populates='roles', secondary='associations_roles_permissions', lazy='selectin', uselist=True)
    users: Mapped[list["UsersORM"]] = relationship(back_populates='role', uselist=False, lazy='selectin')

    def __repr__(self):
        return f'<Roles {self.name}>;{self.permissions};{self.users}>'
class UsersORM(SQLAlchemyBaseUserTableUUID, ModelORM):
    __tablename__ = 'users'
    name: Mapped[str]
    surname: Mapped[str]
    role: Mapped["RolesORM"] = relationship(back_populates='users', uselist=True, lazy='selectin')
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete='CASCADE'))
