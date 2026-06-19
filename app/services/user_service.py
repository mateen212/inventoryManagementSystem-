from typing import Optional, Dict, Any
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut
from app.models.user import User, Role
from app.core.roles import UserRole
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with the specified role."""
        hashed = pwd_context.hash(user_data.password)
        
        # Validate role
        role_name = user_data.role or UserRole.CUSTOMER.value
        if role_name not in [UserRole.ADMIN.value, UserRole.CUSTOMER.value]:
            raise ValueError(f"Invalid role: {role_name}. Only {UserRole.ADMIN.value} and {UserRole.CUSTOMER.value} are allowed.")
        
        role = self.repo.get_role_by_name(role_name)
        if not role:
            # Create role if it doesn't exist
            role = self.repo.create_role(Role(name=role_name))
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed,
            role_id=role.id,
            is_active=True
        )
        return self.repo.create(user)

    def create_admin(self, username: str, email: str, password: str, full_name: str = "Admin") -> User:
        """Create a new admin user."""
        hashed = pwd_context.hash(password)
        role = self.repo.get_role_by_name(UserRole.ADMIN.value)
        if not role:
            role = self.repo.create_role(Role(name=UserRole.ADMIN.value))
        
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed,
            role_id=role.id,
            is_active=True
        )
        return self.repo.create(user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        user = self.repo.get_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(password, hashed_password)

    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    def update_password(self, user_id: int, new_password: str) -> User:
        """Update user password."""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        user.hashed_password = self.hash_password(new_password)
        user.updated_at = datetime.utcnow()
        return self.repo.update(user_id, {"hashed_password": user.hashed_password, "updated_at": user.updated_at})

    def update_user(self, user_id: int, data: Dict[str, Any]) -> User:
        """Update user information."""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Only allow updating specific fields
        allowed_fields = {"full_name", "username"}
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return user
        
        update_data["updated_at"] = datetime.utcnow()
        return self.repo.update(user_id, update_data)

    def disable_user(self, user_id: int) -> User:
        """Disable a user account."""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return self.repo.update(user_id, {"is_active": False, "updated_at": datetime.utcnow()})

    def enable_user(self, user_id: int) -> User:
        """Enable a user account."""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return self.repo.update(user_id, {"is_active": True, "updated_at": datetime.utcnow()})

    def get_by_email(self, email: str) -> Optional[User]:
        return self.repo.get_by_email(email)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)
