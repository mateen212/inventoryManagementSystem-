# Role-Based Access Control (RBAC) Implementation

## Overview

The inventory system implements a strict **role-based access control (RBAC)** system with exactly **two roles**:

1. **Admin** - Full system access with management capabilities
2. **Customer** - Limited access for shopping and order management

## System Architecture

### Role Definitions

Roles are defined in `app/core/roles.py` using an enum and permission mappings:

```python
class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
```

### Database Structure

The roles are stored in the `roles` table and referenced by users via `user.role_id`:

- **roles table**: Contains role definitions (admin, customer)
- **users table**: Contains user data with `role_id` foreign key

## Authentication Flow

### 1. User Registration

**Customer Registration Only:**
- Customers can only register with the `customer` role
- Admin users cannot be created through the registration endpoint
- All new users default to `customer` role

**Endpoint:** `POST /api/auth/register`

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "full_name": "John Doe"
}
```

### 2. User Login

Both roles use the same login endpoint but receive role-specific tokens.

**Endpoint:** `POST /api/auth/login`

```json
{
  "username": "admin_user",
  "password": "admin_password_123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

The JWT token includes:
- `sub`: User ID
- `role`: User's role (admin or customer)
- `exp`: Token expiration time

### 3. Token Verification

All protected endpoints verify the JWT token and check the user's role before granting access.

## Role-Based Access Control

### Admin Role - Full Permissions

#### Authentication
- ✓ Login
- ✓ Logout  
- ✓ Change password
- ✓ Update profile

#### Products
- ✓ View products
- ✓ Search products
- ✓ Create products
- ✓ Edit products
- ✓ Delete products
- ✓ Upload multiple images
- ✓ Generate barcode
- ✓ Generate QR code
- ✓ Manage stock

#### Categories
- ✓ View categories
- ✓ Create categories
- ✓ Edit categories
- ✓ Delete categories

#### Warehouses
- ✓ Create warehouses
- ✓ Edit warehouses
- ✓ Delete warehouses
- ✓ Transfer inventory

#### Suppliers
- ✓ View suppliers
- ✓ Create suppliers
- ✓ Edit suppliers
- ✓ Delete suppliers

#### Customers
- ✓ View all customers
- ✓ Search customers
- ✓ Edit customer information
- ✓ Disable/Enable customer accounts

#### Orders
- ✓ View all orders
- ✓ Update order status
- ✓ Cancel orders
- ✓ Print invoices

#### Reports & Analytics
- ✓ Sales reports
- ✓ Inventory reports
- ✓ Revenue reports
- ✓ Profit reports
- ✓ Export reports (CSV, Excel, JSON, PDF)
- ✓ View analytics dashboard
- ✓ Monthly sales charts
- ✓ Top-selling products
- ✓ Revenue charts
- ✓ Inventory value charts

#### System Management
- ✓ View notifications
- ✓ Send notifications
- ✓ Manage settings (company, currency, tax, email, theme)
- ✓ View users
- ✓ Activate/Suspend users
- ✓ Create backups
- ✓ Restore backups
- ✓ View backup history
- ✓ View activity logs
- ✓ View error logs

### Customer Role - Limited Permissions

#### Authentication
- ✓ Register
- ✓ Login
- ✓ Logout
- ✓ Reset password
- ✓ Update profile (name, email, phone, address)
- ✓ Change password

#### Products
- ✓ View products
- ✓ Search products
- ✓ Filter products
- ✓ View product details
- ✗ Cannot create products
- ✗ Cannot edit products
- ✗ Cannot delete products

#### Shopping Cart
- ✓ Add to cart
- ✓ Remove from cart
- ✓ Update quantity
- ✓ View cart

#### Wishlist
- ✓ Add to wishlist
- ✓ Remove from wishlist
- ✓ Move to cart
- ✓ View wishlist

#### Orders
- ✓ Create orders
- ✓ View own orders
- ✓ View order history
- ✓ Cancel pending orders only
- ✓ Download own invoices
- ✗ Cannot view other customers' orders
- ✗ Cannot change order status
- ✗ Cannot cancel confirmed/shipped orders

#### Profile & Notifications
- ✓ Update own profile
- ✓ Change own password
- ✓ View own notifications
- ✓ Mark notifications as read
- ✓ View dashboard with own orders

#### Restrictions
- ✗ Cannot access admin dashboard
- ✗ Cannot access settings
- ✗ Cannot access reports
- ✗ Cannot access backups/logs
- ✗ Cannot manage users
- ✗ Cannot view analytics
- ✗ Cannot manage products/categories/suppliers

## API Endpoint Protection

### Required Dependencies

All protected endpoints use FastAPI dependencies defined in `app/core/dependencies.py`:

```python
# Require admin role
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    pass

# Require customer role  
@router.get("/")
def get_cart(
    current_user: User = Depends(require_customer),
    db: Session = Depends(get_db)
):
    pass

# Require any authenticated user
@router.put("/{item_id}")
def update_cart_item(
    item_id: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    pass
```

### Response Codes

- **200 OK** - Request successful
- **401 Unauthorized** - User not authenticated, redirect to login
- **403 Forbidden** - User authenticated but lacks required role
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

## Route Protection Summary

### Public Routes (No Authentication Required)
- `POST /api/auth/register` - Customer registration only
- `POST /api/auth/login` - Login for all users
- `GET /api/products/` - View all products
- `GET /api/products/{id}` - View product details
- `GET /api/products/search` - Search products
- `GET /api/categories/` - View categories

### Customer-Only Routes
- `POST /api/carts/add` - Add to cart
- `DELETE /api/carts/{item_id}` - Remove from cart
- `POST /api/orders/` - Create order
- `GET /api/orders/my-orders` - View own orders
- `POST /api/wishlists/add` - Add to wishlist
- `GET /api/notifications/` - View notifications

### Admin-Only Routes
- `POST /api/products/` - Create product
- `PUT /api/products/{id}` - Edit product
- `DELETE /api/products/{id}` - Delete product
- `POST /api/categories/` - Create category
- `POST /api/suppliers/` - Create supplier
- `GET /api/customers/` - List all customers
- `GET /api/orders/admin/all` - View all orders
- `POST /api/settings/*` - Manage settings
- `POST /api/backup/create` - Create backup
- `GET /api/backup/history` - View backups

## Database Initialization

### Initial Setup

Run the database initialization script to create tables and initial roles:

```bash
python init_db.py
```

This script will:
1. Create all database tables
2. Create the `admin` and `customer` roles
3. Prompt you to create an admin user (first time only)

### Admin User Creation

The system will not allow creating admin users through the API. Admin users must be:
1. Created through the initialization script (`init_db.py`)
2. Created by directly inserting into the database

To create additional admin users directly in code:

```python
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

repo = UserRepository(db)
service = UserService(repo)

admin = service.create_admin(
    username="admin_user",
    email="admin@example.com",
    password="secure_password",
    full_name="Administrator"
)
```

## Permission System

### Permission Hierarchy

Permissions are defined as strings and mapped to roles:

```python
# Admin permissions include all operations
"product:create"
"product:delete"
"order:update_status"
"settings:update"

# Customer permissions limited to shopping
"product:read"
"product:search"
"cart:add"
"order:create"
"order:read_own"
```

### Permission Validation

The `app/core/roles.py` module provides utility functions:

```python
from app.core.roles import UserRole, has_permission, has_any_permission

# Check if role has specific permission
if has_permission(user.role, "product:create"):
    # Allow operation
    pass

# Check if role has any of multiple permissions
if has_any_permission(user.role, {"report:sales", "report:revenue"}):
    # Allow operation
    pass
```

## Security Features

### 1. JWT Token Protection
- Tokens include role information
- Tokens expire after configured interval
- Tokens are verified before every protected request

### 2. Role Validation
- Users can only access endpoints matching their role
- No privilege escalation possible through token manipulation
- Role is verified from database on each request

### 3. Password Security
- Passwords hashed with bcrypt
- Minimum password length requirement (8 characters)
- Passwords never stored in plaintext

### 4. User Status
- Disabled user accounts cannot login
- Admin can enable/disable customer accounts

## Configuration

### JWT Settings
Configure in `app/config.py`:

```python
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

### Database
Configure in `app/config.py`:

```python
DATABASE_URL = "sqlite:///./inventory.db"
# or
DATABASE_URL = "postgresql://user:password@localhost/inventory"
```

## Best Practices

1. **Always use role dependencies** - Never skip role checks for convenience
2. **Verify ownership** - For customer endpoints, verify they own the resource
3. **Log admin actions** - Track all admin operations for security
4. **Regular backups** - Admin should create regular database backups
5. **Monitor disabled accounts** - Track why accounts were disabled
6. **Change default passwords** - Change admin password after first login
7. **Use HTTPS** - Always use HTTPS in production for token transmission

## Troubleshooting

### Issue: "Admin access required" Error
**Cause:** User logged in as customer trying to access admin endpoint
**Solution:** Login with admin account or check user role

### Issue: User can't login
**Cause:** Account disabled or incorrect credentials
**Solution:** Check user.is_active flag, verify password, enable account if disabled

### Issue: Role not found error
**Cause:** Database roles not initialized
**Solution:** Run `python init_db.py` to initialize database

### Issue: Token expired
**Cause:** JWT token past expiration time
**Solution:** User should login again to get new token

## Future Enhancements

Potential improvements to the RBAC system:

1. **Dynamic Roles** - Allow creation of custom roles with specific permissions
2. **Permission Inheritance** - Implement role hierarchy
3. **Audit Logging** - Comprehensive logging of all access and modifications
4. **Rate Limiting** - Limit API calls per role
5. **IP Whitelisting** - Restrict admin access to specific IPs
6. **Two-Factor Authentication** - Additional security for admin accounts
7. **Session Management** - Track active sessions and allow remote logout
8. **Resource-level Permissions** - Control access to specific products/orders
