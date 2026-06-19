# Database Management Guide

This guide explains how to use the database initialization, seeding, and reset scripts for the Inventory System.

## Overview of Scripts

### 1. `init_db.py` - Database Initialization
**Purpose**: Creates database tables and initializes roles
**When to use**: First-time setup or after deleting database
**Safe to run multiple times**: Yes (checks for existing data)
**Time**: ~5 seconds

```bash
python init_db.py
```

**What it does**:
- Creates all database tables
- Creates `Admin` role
- Creates `Customer` role
- Verifies database connection

**Output example**:
```
Creating database tables...
✓ Database tables created

Initializing roles...
✓ Created role: admin
✓ Created role: customer

✓ DATABASE INITIALIZATION COMPLETED!

Next steps:
1. Run seeder to add sample data:
   python seeder.py
```

---

### 2. `seeder.py` - Database Seeding
**Purpose**: Populates database with sample data
**When to use**: After `init_db.py` or to add more sample data
**Safe to run multiple times**: Yes (won't duplicate existing data)
**Time**: ~10 seconds
**Creates**: Admin users, customers, suppliers, categories, products

```bash
python seeder.py
```

**What it does**:
- Creates 2 admin users
- Creates 5 sample customers
- Creates 4 suppliers
- Creates 8 product categories
- Creates 12 sample products

**Sample data created**:
```
Admin Users:
  - admin@inventory.local / Admin@12345
  - superadmin@inventory.local / SuperAdmin@12345

Customers:
  - john@example.com / Customer@123
  - jane@example.com / Customer@123
  - bob@example.com / Customer@123
  - alice@example.com / Customer@123
  - charlie@example.com / Customer@123

Suppliers:
  - Tech Supplies Inc.
  - Electronics Wholesale
  - Global Imports Ltd.
  - Premium Products Co.

Categories:
  - Electronics
  - Computers
  - Smartphones
  - Accessories
  - Audio
  - Networking
  - Storage
  - Peripherals

Products: (12 sample products with realistic prices and stock)
```

---

### 3. `setup_database.py` - Complete Setup
**Purpose**: Runs both `init_db.py` and `seeder.py` in sequence
**When to use**: First-time setup, quickest way to get everything ready
**Safe to run multiple times**: Yes
**Time**: ~15 seconds

```bash
python setup_database.py
```

**What it does**:
1. Runs `init_db.py` (create tables and roles)
2. Runs `seeder.py` (populate with sample data)

**Use this for**:
- First-time setup
- Production deployment
- CI/CD pipelines
- Docker container initialization

---

### 4. `reset_database.py` - Database Reset
**Purpose**: Clears all data while keeping database structure and roles
**When to use**: When you want to clear test data but keep the schema
**Safe to run multiple times**: Yes (asks for confirmation)
**Time**: ~5 seconds
**Important**: WILL DELETE ALL DATA - asks for confirmation

```bash
python reset_database.py
```

**What it does**:
- Deletes all users
- Deletes all products
- Deletes all categories
- Deletes all suppliers
- Deletes all orders, carts, wishlists
- Deletes all notifications
- **Preserves**: Database tables and roles

**Usage flow**:
```
python reset_database.py
# Asks for confirmation (type 'yes')
# Clears all data
python seeder.py
# Re-populates with fresh sample data
```

---

## Quick Start Scenarios

### Scenario 1: Fresh Installation
```bash
# Option A (recommended - one command)
python setup_database.py

# Option B (step by step)
python init_db.py
python seeder.py
```

### Scenario 2: Running on Live Server
```bash
# First deployment
python setup_database.py

# To add more sample data later
python seeder.py

# To refresh test data
python reset_database.py
python seeder.py
```

### Scenario 3: Testing Different Data
```bash
# Clear existing data
python reset_database.py

# Load fresh sample data
python seeder.py
```

### Scenario 4: Custom Database Operations
```python
# Python script to directly modify database
from app.database import SessionLocal
from app.models.user import User, Role
from app.core.roles import UserRole

db = SessionLocal()

# Create custom admin user
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

repo = UserRepository(db)
service = UserService(repo)

admin = service.create_admin(
    username="custom_admin",
    email="custom@example.com",
    password="CustomPassword123",
    full_name="Custom Admin"
)

db.close()
```

---

## Database Connection Options

### SQLite (Development/Testing)
```env
DATABASE_URL=sqlite:///./inventory.db
```

File-based database, created automatically in project root

### PostgreSQL (Production Recommended)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db
```

More robust for production, better performance

---

## Useful Database Queries

### Check All Roles
```bash
python -c "
from app.database import SessionLocal
from app.models.user import Role

db = SessionLocal()
roles = db.query(Role).all()
for role in roles:
    print(f'Role: {role.name} (ID: {role.id})')
db.close()
"
```

### Count Users by Role
```bash
python -c "
from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()
admin_count = len([u for u in users if u.role.name == 'admin'])
customer_count = len([u for u in users if u.role.name == 'customer'])
print(f'Admin users: {admin_count}')
print(f'Customer users: {customer_count}')
print(f'Total users: {len(users)}')
db.close()
"
```

### List All Products
```bash
python -c "
from app.database import SessionLocal
from app.models.product import Product

db = SessionLocal()
products = db.query(Product).all()
print(f'Total products: {len(products)}')
for p in products[:5]:
    print(f'  - {p.name}: ${p.price} (Stock: {p.stock})')
if len(products) > 5:
    print(f'  ... and {len(products)-5} more')
db.close()
"
```

### Disable User Account
```bash
python -c "
from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == 'john@example.com').first()
if user:
    user.is_active = False
    db.commit()
    print(f'User {user.email} disabled')
db.close()
"
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"
**Solution**: Run scripts from project root directory
```bash
cd /path/to/inventory_system
python seeder.py
```

### Error: "DatabaseError: table users already exists"
**Solution**: This is normal. The script checks for existing tables.
Just run the seeder to add data.
```bash
python seeder.py
```

### Error: "OperationalError: unable to open database file" (SQLite)
**Solution**: Make sure you have write permissions to project directory
```bash
chmod 755 /path/to/inventory_system
```

### Error: "psycopg2.OperationalError: connection refused" (PostgreSQL)
**Solution**: Check PostgreSQL is running and connection string is correct
```bash
# Test connection
psql -U user -d inventory_db -h localhost

# Update .env with correct settings
```

### Error: "Foreign key constraint failed"
**Solution**: Check that referenced records exist (e.g., category before product)
The seeder handles this automatically by creating in correct order.

### Error: "Admin access required" after seeding
**Solution**: Confirm you're using one of the admin accounts:
- Email: `admin@inventory.local` / Password: `Admin@12345`
- Email: `superadmin@inventory.local` / Password: `SuperAdmin@12345`

---

## Docker Integration

### Dockerfile (example)
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Initialize database when container starts
CMD python init_db.py && python seeder.py && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker Compose
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: inventory_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: inventory_db
    ports:
      - "5432:5432"

  app:
    build: .
    command: sh -c "python init_db.py && python seeder.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://inventory_user:secure_password@postgres:5432/inventory_db
    depends_on:
      - postgres
```

Run with:
```bash
docker-compose up
```

---

## Backup and Restore

### SQLite Backup
```bash
# Create backup
cp inventory.db inventory.db.backup-$(date +%Y%m%d-%H%M%S)

# Restore from backup
cp inventory.db.backup-20240115-120000 inventory.db
```

### PostgreSQL Backup
```bash
# Create backup
pg_dump -U user inventory_db > backup-$(date +%Y%m%d-%H%M%S).sql

# Restore from backup
psql -U user inventory_db < backup-20240115-120000.sql
```

---

## Customizing Seeded Data

Edit `seeder.py` to customize what gets seeded:

```python
# Example: Add more products
products = [
    {
        "name": "Your Custom Product",
        "description": "Description",
        "price": 99.99,
        "stock": 50,
        "sku": "CUSTOM-001",
        "category_id": 1,
        "supplier_id": 1,
    },
    # ... add more
]
```

Then run:
```bash
python seeder.py
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Database Setup

on: [push, pull_request]

jobs:
  setup:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Initialize database
        run: python init_db.py
      
      - name: Seed database
        run: python seeder.py
      
      - name: Run tests
        run: pytest
```

---

## Performance Considerations

### For Development
- SQLite is fine
- Single seeder run is enough
- Reset database between test iterations

### For Production
- Use PostgreSQL
- Run `setup_database.py` once during initial deployment
- Use `seeder.py` only to add more data
- Keep regular backups
- Don't use `reset_database.py` on production without backup

### Optimization
- Add database indexes after seeding
- Set up connection pooling
- Monitor query performance
- Use read replicas for scaling

---

## Support

For more information:
- See `RBAC_IMPLEMENTATION.md` for roles and permissions
- See `DEPLOYMENT_GUIDE.md` for production setup
- See `API_ENDPOINTS.md` for API usage
- See `QUICK_START.md` for getting started
