#!/usr/bin/env python3
"""
Database initialization script.
Creates database tables and initializes roles.
Run seeder.py to add sample data.
"""
import sys
from app.database import engine, SessionLocal
from app.models import Base
from app.models.user import Role
from app.core.roles import UserRole

def init_db():
    """Initialize the database with tables and default roles."""
    print("=" * 60)
    print("INVENTORY SYSTEM - DATABASE INITIALIZATION")
    print("=" * 60)
    
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    db = SessionLocal()
    try:
        # Create roles if they don't exist
        print("\nInitializing roles...")
        for role_name in [UserRole.ADMIN.value, UserRole.CUSTOMER.value]:
            existing_role = db.query(Role).filter(Role.name == role_name).first()
            if not existing_role:
                role = Role(name=role_name)
                db.add(role)
                print(f"✓ Created role: {role_name}")
            else:
                print(f"✓ Role already exists: {role_name}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("✓ DATABASE INITIALIZATION COMPLETED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run seeder to add sample data:")
        print("   python seeder.py")
        print("\n2. Start the application:")
        print("   uvicorn app.main:app --reload")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

