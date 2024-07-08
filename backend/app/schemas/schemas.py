import uuid
from typing import Optional

from pydantic import BaseModel
from fastapi_users import schemas


class PermissionAdd(BaseModel):
    method: str
    name: str
    path: str

    class Config:
        orm_mode = True
        from_attributes = True


class PermissionBase(PermissionAdd):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class RoleAdd(BaseModel):
    name: str

    class Config:
        orm_mode = True
        from_attributes = True


class RoleBase(RoleAdd):
    id: int
    permissions: list[PermissionAdd] = []

    class Config:
        orm_mode = True
        from_attributes = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str
    surname: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    role_id: int


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str
    role_id: int

class ResponseSchemas(BaseModel):
    id: Optional[int] = None
    ok: bool = True
