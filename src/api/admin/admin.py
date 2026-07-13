
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.user import user_crud
from src.deps.database import get_db
from src.deps.permission import require_role
from src.models import User, UserRole
from src.schemas.auth.user import UserListResponse, UserRoleUpdate


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/", response_model=list[UserListResponse])
async def get_all_users(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """
    Gets all users for further operations
    JSON response contains only certain information (name, surname, id ...)
    Current user must be admin for this operation
    """
    return await user_crud.get_all(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.patch("/{user_id}/user_role")
async def change_user_role(
        user_id: int,
        data: UserRoleUpdate,
        current_user: User = Depends(require_role(UserRole.ADMIN)),
        db: AsyncSession = Depends(get_db),
):
    """
    Changes permission of selected user.
    Current user must be admin for this operation
    """
    return await user_crud.change_user_role(
        db=db,
        user_id=user_id,
        obj_in=data,
    )
