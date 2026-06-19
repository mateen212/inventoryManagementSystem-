#!/usr/bin/env python3
"""
Complete Database Setup Script
Initializes database and seeds all data in one command.
Safe to run multiple times - won't duplicate existing data.
"""
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and report status."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode == 0:
            print(f"✓ {description} - SUCCESS")
            return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e}")
        return False
    return False

def main():
    print("\n" + "=" * 60)
    print("INVENTORY SYSTEM - COMPLETE DATABASE SETUP")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Initialize database tables")
    print("2. Create roles (Admin and Customer)")
    print("3. Seed sample data (admin users, customers, products, etc.)")
    print("\nNote: Safe to run multiple times - won't duplicate data")
    print("=" * 60)
    
    # Step 1: Initialize database
    if not run_command("python init_db.py", "Step 1: Initialize Database"):
        print("\n✗ Setup failed at database initialization")
        sys.exit(1)
    
    # Step 2: Seed database
    if not run_command("python seeder.py", "Step 2: Seed Database with Sample Data"):
        print("\n✗ Setup failed at database seeding")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ COMPLETE DATABASE SETUP FINISHED SUCCESSFULLY!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Start the application:")
    print("   uvicorn app.main:app --reload")
    print("\n2. Access the API:")
    print("   http://localhost:8000")
    print("\n3. View API documentation:")
    print("   http://localhost:8000/docs")
    print("\n4. Login with admin account:")
    print("   Email: admin@inventory.local")
    print("   Password: Admin@12345")
    print("\n5. Or login with second admin account:")
    print("   Email: superadmin@inventory.local")
    print("   Password: SuperAdmin@12345")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
