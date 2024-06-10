from fastapi import Depends, HTTPException, status

from src.users.manager import current_active_user
from src.users.models import CustomUsersDB


def require_role(required_roles: list):
    def role_dependency(current_user: CustomUsersDB = Depends(current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return role_dependency
