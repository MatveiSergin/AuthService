import uuid
from typing import Optional

from pydantic import BaseModel
from fastapi_users import schemas


class PermissionAdd(BaseModel):
    method: str
    name: str
    path: str

    class Config:
        from_attributes = True


class PermissionBase(PermissionAdd):
    id: int

    class Config:
        from_attributes = True


class RoleAdd(BaseModel):
    name: str

    class Config:
        from_attributes = True


class RoleBase(RoleAdd):
    id: int
    permissions: list[PermissionAdd] = []

    class Config:
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


class RequestAccess(BaseModel):
    path: str
    method: str

    def __repr__(self):
        return f"path: {self.path}, method: {self.method}"
class ResponseCheck(BaseModel):
    success: bool
