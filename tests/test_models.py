import pytest
from app.models.user import User, Role
from app.models.product import Product

def test_user_creation():
    role = Role(name="admin")
    user = User(username="test", email="test@example.com", hashed_password="hashed", role=role)
    assert user.email == "test@example.com"
