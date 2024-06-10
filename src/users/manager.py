from typing import Optional

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers

from .auth import auth_backend
from .models import CustomUsersDB, get_user_db
from ..config import SECRET_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[CustomUsersDB, int]):
    reset_password_token_secret = SECRET_TOKEN
    verification_token_secret = SECRET_TOKEN

    async def on_after_register(self, user: CustomUsersDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[CustomUsersDB, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
