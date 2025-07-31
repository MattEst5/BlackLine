from fastapi import Depends, HTTPException, status
from app.utils import auth_handler
from app.models import user as models

def require_admin(current_user: models.User = Depends(auth_handler.get_current_user)):
    if current_user.role not in ("admin", "dev"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return current_user