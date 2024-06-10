from datetime import datetime
from typing import Optional

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Field, Relationship
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.users.schemas import RoleEnum


class CustomUsersDB(SQLModelBaseUserDB, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, nullable=False, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    is_verified: bool = Field(True, nullable=False)
    manager_id: int = Field(foreign_key="users.id", nullable=True)

    created_at: datetime = Field(default_factory=datetime.now)

    role: RoleEnum = Field(
        default=RoleEnum.USER
    )

    request_logs: list["MessageDB"] = Relationship(back_populates="author")
    manager: Optional["CustomUsersDB"] = Relationship()


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, CustomUsersDB)
