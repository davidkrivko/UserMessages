from enum import Enum
from typing import Optional, List

from fastapi_users import schemas


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    MANAGER = "MANAGER"


class UserBase(schemas.BaseUser[int]):
    first_name: Optional[str]
    last_name: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    first_name: Optional[str]
    last_name: Optional[str]


class UserRead(UserBase):
    id: int
    role: RoleEnum

    class Config:
        orm_mode = True


class UserUpdate(schemas.CreateUpdateDictModel):
    first_name: Optional[str]
    last_name: Optional[str]


class UserAdminUpdate(UserBase):
    role: RoleEnum


class UserManagerUpdate(schemas.CreateUpdateDictModel):
    manager_id: Optional[int]
    user_ids: Optional[List[int]]
