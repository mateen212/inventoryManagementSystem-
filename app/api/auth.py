from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut, Token, UserLogin, UserChangePassword
from app.core.auth import create_access_token, get_current_user
from app.core.roles import UserRole
from app.core.dependencies import require_authenticated
from app.models.user import User
from app.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new customer account."""
    # Customers can only register as CUSTOMER role
    if user_data.role and user_data.role != UserRole.CUSTOMER.value:
        raise HTTPException(
            status_code=400, 
            detail="Customers can only register as customer role"
        )
    
    repo = UserRepository(db)
    service = UserService(repo)
    existing = service.get_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Force role to CUSTOMER for registration
    user_data.role = UserRole.CUSTOMER.value
    user = service.create_user(user_data)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with username and password."""
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")
    
    access_token = create_access_token(data={
        "sub": str(user.id), 
        "role": user.role.name if user.role else UserRole.CUSTOMER.value
    })
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(require_authenticated)):
    """Logout current user."""
    return {"message": "Successfully logged out"}

@router.post("/change-password")
def change_password(
    data: UserChangePassword, 
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Change password for authenticated user."""
    repo = UserRepository(db)
    service = UserService(repo)
    
    # Verify old password
    if not service.verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    # Update password
    service.update_password(current_user.id, data.new_password)
    return {"message": "Password changed successfully"}

@router.post("/update-profile", response_model=UserOut)
def update_profile(
    data: dict,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Update user profile."""
    repo = UserRepository(db)
    service = UserService(repo)
    
    # Only allow updating allowed fields
    allowed_fields = {"full_name", "username"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    updated_user = service.update_user(current_user.id, update_data)
    return updated_user
