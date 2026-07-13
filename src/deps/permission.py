
from fastapi import Depends, HTTPException, status

from src.deps.user import get_current_user
from src.models.auth.user import User
from src.models.auth.user import UserRole


"""
    Function require_admin is used to check if selected user is ADMIN. Works only for admin checking 
    By require_role you can check if a user has any of the specified rights.
    Both of the functions must be used via Dependency injection
"""

async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """ Requires user to be admin """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )
    return current_user


def require_role(*roles: UserRole):
    async def checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        """ Checks users permission """
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return checker
