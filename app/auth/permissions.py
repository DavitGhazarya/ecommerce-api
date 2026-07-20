from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.user import UserRole


def require_roles(*roles):

    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return current_user

    return checker


admin_only = require_roles(UserRole.ADMIN)

seller_only = require_roles(UserRole.SELLER)

admin_or_seller = require_roles(
    UserRole.ADMIN,
    UserRole.SELLER
)