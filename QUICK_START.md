# Quick Start Guide - RBAC System

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database & Seed Data

**Option A: Complete Setup (Recommended)**
```bash
python setup_database.py
```
This will:
- Create database tables
- Create roles (Admin and Customer)
- Add sample data (admin users, customers, products, suppliers, etc.)

**Option B: Step by Step**
```bash
# Step 1: Initialize database (creates tables and roles)
python init_db.py

# Step 2: Seed database with sample data
python seeder.py
```

### 3. Start Application
```bash
uvicorn app.main:app --reload
```

Application will be available at: `http://localhost:8000`

### 4. Access API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Available Database Scripts

### `init_db.py` - Initialize Database
Creates database tables and roles only (no sample data)
```bash
python init_db.py
```

### `seeder.py` - Add Sample Data
Populates database with:
- 2 admin users
- 5 sample customers
- 4 suppliers
- 8 product categories
- 12 sample products

Safe to run multiple times (won't duplicate existing data)
```bash
python seeder.py
```

### `setup_database.py` - Complete Setup
Combines both `init_db.py` and `seeder.py` in one command
```bash
python setup_database.py
```

### `reset_database.py` - Clear Data
Deletes all data but keeps database structure and roles
Safe to run, asks for confirmation before deleting
```bash
python reset_database.py
python seeder.py  # Re-populate after reset
```

For detailed database management, see `DATABASE_MANAGEMENT.md`

---

## User Roles

### Admin Role
**Full access to all admin features**
- Manage products, categories, suppliers
- View and manage customers
- View all orders and manage order status
- Create and restore backups
- Manage system settings
- View analytics and reports

### Customer Role
**Limited access for shopping**
- Browse and search products
- Manage shopping cart
- Create orders
- Manage wishlist
- View own orders and invoices
- Update own profile

---

## Common Tasks

### As Admin

#### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin_user&password=YourSecurePassword123"
```

#### Create Product
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/products/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Pro",
    "description": "High-performance laptop",
    "price": 1299.99,
    "stock": 10,
    "category_id": 1,
    "supplier_id": 1,
    "sku": "LAP-001"
  }'
```

#### View All Customers
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/customers/?skip=0&limit=100" \
  -H "Authorization: Bearer $TOKEN"
```

#### View All Orders
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/orders/admin/all?skip=0&limit=100" \
  -H "Authorization: Bearer $TOKEN"
```

#### Update Order Status
```bash
TOKEN="your_access_token_here"

curl -X PUT "http://localhost:8000/api/orders/1/status?status=shipped" \
  -H "Authorization: Bearer $TOKEN"
```

#### Create Backup
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/backup/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Daily backup"
  }'
```

---

### As Customer

#### Register
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "full_name": "John Doe"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePassword123"
```

#### View Products
```bash
curl -X GET "http://localhost:8000/api/products/?skip=0&limit=100"
```

#### Search Products
```bash
curl -X GET "http://localhost:8000/api/products/search?q=laptop"
```

#### Add to Cart
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/carts/add?product_id=1&quantity=2" \
  -H "Authorization: Bearer $TOKEN"
```

#### View Cart
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/carts/" \
  -H "Authorization: Bearer $TOKEN"
```

#### Add to Wishlist
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/wishlists/add?product_id=5" \
  -H "Authorization: Bearer $TOKEN"
```

#### Create Order
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/orders/" \
  -H "Authorization: Bearer $TOKEN"
```

#### View My Orders
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/orders/my-orders?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

#### Update Profile
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/auth/update-profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John D Smith",
    "username": "john_smith"
  }'
```

#### Change Password
```bash
TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/auth/change-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePassword123",
    "new_password": "NewSecurePassword456"
  }'
```

#### View Notifications
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/notifications/" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Environment Variables

Configure in `app/config.py`:

```python
# Database
DATABASE_URL = "sqlite:///./inventory.db"

# Security
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Application
APP_NAME = "Inventory Management System"
DEBUG = False  # Set to True only in development
```

---

## Common Errors & Solutions

### "Admin access required"
**Problem**: Trying to access admin endpoint as customer
**Solution**: Use admin account or make request available to customers

### "Not authenticated"
**Problem**: No token provided or token expired
**Solution**: Login again with `POST /api/auth/login`

### "Invalid token"
**Problem**: Token is malformed or tampered with
**Solution**: Login again to get new token

### "Email already registered"
**Problem**: Email already exists in system
**Solution**: Use different email or login with existing account

### "Incorrect username or password"
**Problem**: Wrong credentials provided
**Solution**: Check username and password spelling

### "User account is disabled"
**Problem**: Admin disabled the account
**Solution**: Contact admin to re-enable account

---

## Security Best Practices

1. **Change Default Admin Password**
   - After first login, change admin password immediately
   - Use strong password with mix of uppercase, lowercase, numbers, symbols

2. **Use HTTPS in Production**
   - Never transmit tokens over plain HTTP
   - Always use HTTPS with valid SSL certificates

3. **Store Tokens Securely**
   - Never share tokens with anyone
   - Don't store tokens in version control
   - Use secure storage mechanisms

4. **Regular Backups**
   - Admin should create regular backups
   - Store backups in secure location
   - Test restore procedures

5. **Monitor Access**
   - Review customer account creation
   - Check for suspicious login attempts
   - Monitor backup creation and restores

6. **Update Regularly**
   - Keep dependencies updated
   - Apply security patches
   - Review and update permissions

---

## Database Queries (Direct)

### View All Roles
```sql
SELECT * FROM roles;
```

### View All Users with Roles
```sql
SELECT u.id, u.username, u.email, r.name as role
FROM users u
JOIN roles r ON u.role_id = r.id;
```

### View Admin Users
```sql
SELECT u.id, u.username, u.email
FROM users u
JOIN roles r ON u.role_id = r.id
WHERE r.name = 'admin';
```

### View Customer Users
```sql
SELECT u.id, u.username, u.email
FROM users u
JOIN roles r ON u.role_id = r.id
WHERE r.name = 'customer';
```

### Disable User
```sql
UPDATE users SET is_active = FALSE WHERE id = 1;
```

### Enable User
```sql
UPDATE users SET is_active = TRUE WHERE id = 1;
```

---

## Testing Checklist

- [ ] Admin can login
- [ ] Customer can register
- [ ] Customer can login
- [ ] Admin can create product
- [ ] Customer cannot create product
- [ ] Admin can view all customers
- [ ] Customer cannot view other customers
- [ ] Admin can view all orders
- [ ] Customer can only see own orders
- [ ] Admin can create backup
- [ ] Customer cannot create backup
- [ ] Token expires correctly
- [ ] Invalid token rejected
- [ ] Disabled user cannot login

---

## Directory Structure

```
inventory_system/
├── app/
│   ├── api/                 # API endpoints
│   ├── core/               # Core functionality
│   ├── models/             # Database models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── static/             # Static files (CSS, JS)
│   ├── templates/          # HTML templates
│   ├── web/                # Web routes
│   ├── config.py           # Configuration
│   ├── database.py         # Database setup
│   └── main.py             # Application entry point
├── tests/                  # Test files
├── init_db.py              # Database initialization
├── RBAC_IMPLEMENTATION.md  # RBAC documentation
├── API_ENDPOINTS.md        # API reference
├── IMPLEMENTATION_SUMMARY.md # Implementation overview
└── requirements.txt        # Python dependencies
```

---

## Support & Documentation

- **RBAC Documentation**: See `RBAC_IMPLEMENTATION.md`
- **API Reference**: See `API_ENDPOINTS.md`
- **Full Summary**: See `IMPLEMENTATION_SUMMARY.md`
- **FastAPI Docs**: http://localhost:8000/docs
- **Role Definitions**: Check `app/core/roles.py`

---

## Next Steps

1. ✅ Initialize database (`python init_db.py`)
2. ✅ Start application (`uvicorn app.main:app --reload`)
3. ✅ Test admin endpoints
4. ✅ Create test customer account
5. ✅ Test customer endpoints
6. ✅ Review API documentation at `/docs`
7. ✅ Deploy to production when ready
