from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.database import get_session
from src.users.models import CustomUsersDB
from src.users.permissions import require_role
from src.users.schemas import RoleEnum

users_router = APIRouter(
    prefix="/users",
)


@users_router.patch("/{user_id}/manager/")
async def set_manager(
        user_id: int, manager_id: int | None = None,
        session: AsyncSession = Depends(get_session),
        client: CustomUsersDB = Depends(require_role(["ADMIN"]))
):
    user = await session.execute(select(CustomUsersDB).filter(CustomUsersDB.id == user_id))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if manager_id is not None:
        manager = await session.execute(select(CustomUsersDB).filter(
            (CustomUsersDB.id == manager_id)
            & (CustomUsersDB.role.in_([RoleEnum.MANAGER, RoleEnum.ADMIN]))
        ))
        manager = manager.first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")

    user.manager_id = manager_id
    await session.commit()
    await session.refresh(user)
    return user


@users_router.patch("/{user_id}/role/{role}")
async def change_role(
        user_id: int, role: str,
        session: AsyncSession = Depends(get_session),
        client: CustomUsersDB = Depends(require_role(["ADMIN"]))
):
    user = await session.execute(select(CustomUsersDB).filter(CustomUsersDB.id == user_id))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if role not in RoleEnum.__members__:
        raise HTTPException(status_code=400, detail="Role is not correct")

    user.role = role
    await session.commit()
    await session.refresh(user)
    return user
