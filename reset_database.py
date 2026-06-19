#!/usr/bin/env python3
"""
Database Reset Script
Clears all data and re-seeds the database.
Use this to refresh the database on live server while keeping structure.
"""
import sys
from app.database import SessionLocal, engine
from app.models import Base
from app.models.user import User, Role
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.invoice import Invoice
from app.models.wishlist import Wishlist
from app.models.notification import Notification

def confirm_reset():
    """Ask user to confirm database reset."""
    print("\n" + "=" * 60)
    print("⚠️  WARNING: DATABASE RESET")
    print("=" * 60)
    print("\nThis will DELETE ALL DATA from the database:")
    print("- Users")
    print("- Products")
    print("- Categories")
    print("- Suppliers")
    print("- Orders")
    print("- Carts")
    print("- And more...")
    print("\nDatabase structure (tables) will remain intact.")
    print("\nAfter reset, you'll need to run seeder.py to re-populate data.")
    response = input("\nType 'yes' to confirm: ").strip().lower()
    return response == 'yes'

def reset_database():
    """Clear all data from database."""
    if not confirm_reset():
        print("\n✗ Reset cancelled.")
        return False
    
    print("\n" + "=" * 60)
    print("CLEARING DATABASE...")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Delete all data (keeping roles)
        print("\nDeleting users...")
        db.query(User).delete()
        
        print("Deleting products...")
        db.query(Product).delete()
        
        print("Deleting categories...")
        db.query(Category).delete()
        
        print("Deleting suppliers...")
        db.query(Supplier).delete()
        
        print("Deleting cart items...")
        db.query(CartItem).delete()
        
        print("Deleting carts...")
        db.query(Cart).delete()
        
        print("Deleting order items...")
        db.query(OrderItem).delete()
        
        print("Deleting orders...")
        db.query(Order).delete()
        
        print("Deleting invoices...")
        db.query(Invoice).delete()
        
        print("Deleting wishlists...")
        db.query(Wishlist).delete()
        
        print("Deleting notifications...")
        db.query(Notification).delete()
        
        db.commit()
        
        print("\n✓ All data deleted successfully!")
        print("✓ Roles preserved (Admin and Customer)")
        print("\nNext step: Run 'python seeder.py' to re-populate data")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during reset: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("INVENTORY SYSTEM - DATABASE RESET")
    print("=" * 60)
    
    success = reset_database()
    
    if success:
        print("=" * 60 + "\n")
        sys.exit(0)
    else:
        print("=" * 60 + "\n")
        sys.exit(1)
