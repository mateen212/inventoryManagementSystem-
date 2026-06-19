#!/usr/bin/env python3
"""
Database Seeder Script
Populates the database with initial data for the inventory system.
Can be safely run multiple times - checks for existing data before adding.
"""
import sys
from datetime import datetime
from app.database import engine, SessionLocal
from app.models import Base
from app.models.user import Role, User
from sqlalchemy import or_
from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.core.roles import UserRole
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """Create all database tables if they don't exist."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created/verified")

def seed_roles(db):
    """Create default roles if they don't exist."""
    print("\nSeeding roles...")
    
    roles_to_create = [
        UserRole.ADMIN.value,
        UserRole.CUSTOMER.value,
    ]
    
    for role_name in roles_to_create:
        existing_role = db.query(Role).filter(Role.name == role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            db.add(role)
            print(f"✓ Created role: {role_name}")
        else:
            print(f"✓ Role already exists: {role_name}")
    
    db.commit()

def seed_admin_users(db):
    """Create default admin users if they don't exist."""
    print("\nSeeding admin users...")
    
    admin_role = db.query(Role).filter(Role.name == UserRole.ADMIN.value).first()
    if not admin_role:
        print("✗ Admin role not found. Run seed_roles first.")
        return
    
    admin_users = [
        {
            "username": "admin",
            "email": "admin@inventory.local",
            "password": "Admin@12345",
            "full_name": "System Administrator",
        },
        {
            "username": "superadmin",
            "email": "superadmin@inventory.local",
            "password": "SuperAdmin@12345",
            "full_name": "Super Administrator",
        },
    ]
    
    for admin_data in admin_users:
        # Check existing by email OR username to avoid unique constraint errors
        existing_user = db.query(User).filter(
            or_(User.email == admin_data["email"], User.username == admin_data["username"])
        ).first()
        if not existing_user:
            hashed_password = pwd_context.hash(admin_data["password"])
            user = User(
                username=admin_data["username"],
                email=admin_data["email"],
                full_name=admin_data["full_name"],
                hashed_password=hashed_password,
                role_id=admin_role.id,
                is_active=True
            )
            db.add(user)
            print(f"✓ Created admin user: {admin_data['email']} (password: {admin_data['password']})")
        else:
            # Determine whether it's by email or username
            if existing_user.email == admin_data["email"]:
                print(f"✓ Admin user already exists: {admin_data['email']}")
            else:
                print(f"⚠ Skipping admin creation; username already taken: {admin_data['username']}")
    
    db.commit()

def seed_customers(db):
    """Create sample customer users if they don't exist."""
    print("\nSeeding customer users...")
    
    customer_role = db.query(Role).filter(Role.name == UserRole.CUSTOMER.value).first()
    if not customer_role:
        print("✗ Customer role not found. Run seed_roles first.")
        return
    
    customers = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "Customer@123",
            "full_name": "John Doe",
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "password": "Customer@123",
            "full_name": "Jane Smith",
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "password": "Customer@123",
            "full_name": "Bob Wilson",
        },
        {
            "username": "alice_brown",
            "email": "alice@example.com",
            "password": "Customer@123",
            "full_name": "Alice Brown",
        },
        {
            "username": "charlie_davis",
            "email": "charlie@example.com",
            "password": "Customer@123",
            "full_name": "Charlie Davis",
        },
    ]
    
    created_count = 0
    for customer_data in customers:
        existing_user = db.query(User).filter(User.email == customer_data["email"]).first()
        if not existing_user:
            hashed_password = pwd_context.hash(customer_data["password"])
            user = User(
                username=customer_data["username"],
                email=customer_data["email"],
                full_name=customer_data["full_name"],
                hashed_password=hashed_password,
                role_id=customer_role.id,
                is_active=True
            )
            db.add(user)
            created_count += 1
        else:
            print(f"  ℹ Customer already exists: {customer_data['email']}")
    
    if created_count > 0:
        db.commit()
        print(f"✓ Created {created_count} customer user(s)")
    else:
        print("✓ All customer users already exist")

def seed_suppliers(db):
    """Create sample suppliers if they don't exist."""
    print("\nSeeding suppliers...")
    
    suppliers = [
        {
            "name": "Tech Supplies Inc.",
            "contact_person": "John Smith",
            "email": "john@techsupplies.com",
            "phone": "+1-800-123-4567",
            "address": "123 Tech Street, San Francisco, CA 94105",
        },
        {
            "name": "Electronics Wholesale",
            "contact_person": "Jane Johnson",
            "email": "jane@electronicsws.com",
            "phone": "+1-800-234-5678",
            "address": "456 Electronics Ave, New York, NY 10001",
        },
        {
            "name": "Global Imports Ltd.",
            "contact_person": "Mike Chen",
            "email": "mike@globalimports.com",
            "phone": "+1-800-345-6789",
            "address": "789 Import Road, Los Angeles, CA 90001",
        },
        {
            "name": "Premium Products Co.",
            "contact_person": "Sarah Williams",
            "email": "sarah@premiumproducts.com",
            "phone": "+1-800-456-7890",
            "address": "321 Premium Way, Chicago, IL 60601",
        },
    ]
    
    created_count = 0
    for supplier_data in suppliers:
        existing_supplier = db.query(Supplier).filter(Supplier.email == supplier_data["email"]).first()
        if not existing_supplier:
            supplier = Supplier(**supplier_data)
            db.add(supplier)
            created_count += 1
        else:
            print(f"  ℹ Supplier already exists: {supplier_data['name']}")
    
    if created_count > 0:
        db.commit()
        print(f"✓ Created {created_count} supplier(s)")
    else:
        print("✓ All suppliers already exist")

def seed_categories(db):
    """Create sample product categories if they don't exist."""
    print("\nSeeding categories...")
    
    categories = [
        {"name": "Electronics", "description": "Electronic devices and gadgets"},
        {"name": "Computers", "description": "Laptops, desktops, and computer components"},
        {"name": "Smartphones", "description": "Mobile phones and accessories"},
        {"name": "Accessories", "description": "Phone and computer accessories"},
        {"name": "Audio", "description": "Headphones, speakers, and audio equipment"},
        {"name": "Networking", "description": "Network devices and equipment"},
        {"name": "Storage", "description": "Hard drives, SSDs, and storage solutions"},
        {"name": "Peripherals", "description": "Keyboards, mice, and other peripherals"},
    ]
    
    created_count = 0
    for cat_data in categories:
        existing_category = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing_category:
            category = Category(**cat_data)
            db.add(category)
            created_count += 1
        else:
            print(f"  ℹ Category already exists: {cat_data['name']}")
    
    if created_count > 0:
        db.commit()
        print(f"✓ Created {created_count} category/categories")
    else:
        print("✓ All categories already exist")

def seed_products(db):
    """Create sample products if they don't exist."""
    print("\nSeeding products...")
    
    # Get categories
    electronics_cat = db.query(Category).filter(Category.name == "Electronics").first()
    computers_cat = db.query(Category).filter(Category.name == "Computers").first()
    smartphones_cat = db.query(Category).filter(Category.name == "Smartphones").first()
    audio_cat = db.query(Category).filter(Category.name == "Audio").first()
    accessories_cat = db.query(Category).filter(Category.name == "Accessories").first()
    
    # Get supplier
    supplier = db.query(Supplier).first()
    
    if not supplier:
        print("✗ No suppliers found. Run seed_suppliers first.")
        return
    
    products = [
        {
            "name": "Dell XPS 13 Laptop",
            "description": "Powerful and portable laptop with Intel Core i7",
            "price": 1299.99,
            "stock": 15,
            "sku": "DELL-XPS-13",
            "category_id": computers_cat.id if computers_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "MacBook Pro 16",
            "description": "Professional laptop with M2 Pro chip",
            "price": 2499.99,
            "stock": 8,
            "sku": "APPLE-MBP-16",
            "category_id": computers_cat.id if computers_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "iPhone 14 Pro",
            "description": "Latest iPhone with A16 Bionic chip",
            "price": 999.99,
            "stock": 25,
            "sku": "APPLE-IP14P",
            "category_id": smartphones_cat.id if smartphones_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "Samsung Galaxy S23",
            "description": "Flagship Android smartphone",
            "price": 899.99,
            "stock": 20,
            "sku": "SAMSUNG-S23",
            "category_id": smartphones_cat.id if smartphones_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "description": "Premium noise-cancelling headphones",
            "price": 399.99,
            "stock": 30,
            "sku": "SONY-WH1000XM5",
            "category_id": audio_cat.id if audio_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "Apple AirPods Pro",
            "description": "Wireless earbuds with active noise cancellation",
            "price": 249.99,
            "stock": 40,
            "sku": "APPLE-AIRPODS-PRO",
            "category_id": audio_cat.id if audio_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "USB-C Charging Cable",
            "description": "High-speed USB-C cable, 2 meters",
            "price": 19.99,
            "stock": 100,
            "sku": "CABLE-USB-C-2M",
            "category_id": accessories_cat.id if accessories_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with USB receiver",
            "price": 29.99,
            "stock": 50,
            "sku": "MOUSE-WIRELESS",
            "category_id": accessories_cat.id if accessories_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "Mechanical Keyboard",
            "description": "RGB mechanical keyboard with Cherry MX switches",
            "price": 149.99,
            "stock": 35,
            "sku": "KEYBOARD-MECH-RGB",
            "category_id": accessories_cat.id if accessories_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "4TB External SSD",
            "description": "Fast external SSD storage",
            "price": 399.99,
            "stock": 12,
            "sku": "SSD-EXT-4TB",
            "category_id": electronics_cat.id if electronics_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "WiFi 6 Router",
            "description": "High-speed WiFi 6 router with mesh support",
            "price": 299.99,
            "stock": 18,
            "sku": "ROUTER-WIFI6",
            "category_id": electronics_cat.id if electronics_cat else None,
            "supplier_id": supplier.id,
        },
        {
            "name": "4K Webcam",
            "description": "Professional 4K webcam for streaming",
            "price": 199.99,
            "stock": 22,
            "sku": "WEBCAM-4K",
            "category_id": accessories_cat.id if accessories_cat else None,
            "supplier_id": supplier.id,
        },
    ]
    
    created_count = 0
    for product_data in products:
        existing_product = db.query(Product).filter(Product.sku == product_data["sku"]).first()
        if not existing_product:
            # Map keys to model fields (price -> selling_price, stock -> quantity)
            p = product_data.copy()
            if "price" in p:
                p["selling_price"] = p.pop("price")
            if "stock" in p:
                p["quantity"] = p.pop("stock")
            product = Product(**p)
            db.add(product)
            created_count += 1
        else:
            print(f"  ℹ Product already exists: {product_data['name']}")
    
    if created_count > 0:
        db.commit()
        print(f"✓ Created {created_count} product(s)")
    else:
        print("✓ All products already exist")

def main():
    """Run all seeding operations."""
    print("=" * 60)
    print("INVENTORY SYSTEM - DATABASE SEEDER")
    print("=" * 60)
    
    try:
        # Create tables first
        create_tables()
        
        # Open database session
        db = SessionLocal()
        
        try:
            # Seed data
            seed_roles(db)
            seed_admin_users(db)
            seed_customers(db)
            seed_suppliers(db)
            seed_categories(db)
            seed_products(db)
            
            print("\n" + "=" * 60)
            print("✓ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\nAdmin Users Created:")
            print("  1. admin@inventory.local / Admin@12345")
            print("  2. superadmin@inventory.local / SuperAdmin@12345")
            print("\nSample Customer Users Created:")
            print("  - john@example.com / Customer@123")
            print("  - jane@example.com / Customer@123")
            print("  - bob@example.com / Customer@123")
            print("  - alice@example.com / Customer@123")
            print("  - charlie@example.com / Customer@123")
            print("\nNote: You can run this script again safely - it won't duplicate existing data.")
            print("=" * 60 + "\n")
            
        finally:
            db.close()
    
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
