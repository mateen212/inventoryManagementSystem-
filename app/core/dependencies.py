from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_user
from app.core.roles import UserRole
from app.models.user import User

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require admin role."""
    if not current_user.role or current_user.role.name != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def require_customer(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require customer role."""
    if not current_user.role or current_user.role.name != UserRole.CUSTOMER.value:
        raise HTTPException(status_code=403, detail="Customer access required")
    return current_user

def require_authenticated(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require any authenticated user."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return current_user

def check_role(required_role: UserRole):
    """Factory function to create a dependency for a specific role."""
    async def check_user_role(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.role or current_user.role.name != required_role.value:
            raise HTTPException(
                status_code=403, 
                detail=f"{required_role.value.title()} access required"
            )
        return current_user
    return check_user_role
