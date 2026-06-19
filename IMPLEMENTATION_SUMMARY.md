# Role-Based Access Control (RBAC) Implementation - Summary

## Overview

A comprehensive role-based access control system has been implemented with **exactly two roles**:

1. **Admin** - Complete system management and administrative access
2. **Customer** - Limited shopping and account management access

## What Was Implemented

### 1. Role Management System

#### New Files Created:
- **`app/core/roles.py`** - Enum and permission definitions for Admin and Customer roles
  - Defines `UserRole` enum with ADMIN and CUSTOMER values
  - Maps permissions to each role
  - Provides utility functions for permission checks

#### Modified Files:
- **`app/models/user.py`** - Enhanced User and Role models
  - Added proper relationships between User and Role
  - Added role_id as nullable=False (required)
  - Added __repr__ methods for debugging

### 2. Authentication System Enhancements

#### Modified Files:
- **`app/api/auth.py`** - Complete authentication endpoints
  - `POST /api/auth/register` - Customer registration only (forces customer role)
  - `POST /api/auth/login` - Login for all users
  - `GET /api/auth/me` - Get current user profile
  - `POST /api/auth/logout` - Logout endpoint
  - `POST /api/auth/change-password` - Change password
  - `POST /api/auth/update-profile` - Update profile

- **`app/services/user_service.py`** - Enhanced user service
  - Role validation in user creation
  - Password hashing and verification methods
  - User update and profile management methods
  - User enable/disable functionality

- **`app/schemas/user.py`** - Updated schemas
  - Added `UserChangePassword` schema
  - Enhanced `UserCreate` with role field validation
  - Added password constraints

### 3. Role-Based Access Control

#### New Files Created:
- **`app/core/dependencies.py`** - Updated with role-checking dependencies
  - `require_admin()` - Dependency for admin-only routes
  - `require_customer()` - Dependency for customer-only routes
  - `require_authenticated()` - Dependency for any authenticated user
  - `check_role()` - Factory function for role checking

### 4. Protected API Endpoints

All endpoints have been updated with proper role-based access control:

#### Admin-Only Endpoints:
- **Products**: Create, Edit, Delete, Upload Images, Generate Barcode/QR Code, Manage Stock
- **Categories**: Create, Edit, Delete
- **Suppliers**: Create, Edit, Delete
- **Customers**: View, Search, Edit, Disable/Enable
- **Orders**: View all, Update status, Cancel, Print invoices
- **Settings**: Company info, Currency, Tax, Email, Theme
- **Backup**: Create, Restore, Delete, View history
- **Notifications**: Send to user or broadcast

#### Customer-Only/Authenticated Endpoints:
- **Products**: View, Search (read-only)
- **Cart**: Add, Remove, Update quantity
- **Wishlist**: Add, Remove, Move to cart
- **Orders**: Create, View own orders, Cancel pending, Download invoices
- **Profile**: Update own profile, Change password
- **Notifications**: View own, Mark as read

#### Protected Files:
- `app/api/auth.py` - Authentication endpoints
- `app/api/products.py` - Product management (enhanced)
- `app/api/categories.py` - Category management (enhanced)
- `app/api/suppliers.py` - Supplier management (enhanced)
- `app/api/customers.py` - Customer management (new implementation)
- `app/api/carts.py` - Shopping cart (new implementation)
- `app/api/orders.py` - Order management (new implementation)
- `app/api/wishlists.py` - Wishlist management (new implementation)
- `app/api/invoices.py` - Invoice management (new implementation)
- `app/api/notifications.py` - Notifications (new implementation)
- `app/api/backup.py` - Backup management (new implementation)
- `app/api/settings.py` - Settings management (new implementation)

### 5. Database Utilities

#### New Files Created:
- **`init_db.py`** - Database initialization script
  - Creates all database tables
  - Initializes Admin and Customer roles
  - Prompts for admin user creation
  - Can be re-run safely (checks for existing data)

#### Modified Files:
- **`app/repositories/base_repository.py`** - Fixed and enhanced
  - Cleaned up duplicate code
  - Enhanced `update()` method to support both dict and kwargs
  - Better error handling

### 6. Documentation

#### New Files Created:
- **`RBAC_IMPLEMENTATION.md`** - Comprehensive RBAC documentation
  - System architecture overview
  - Authentication flow
  - Complete role permissions list
  - API endpoint protection summary
  - Security features and best practices
  - Troubleshooting guide
  - Future enhancement ideas

- **`API_ENDPOINTS.md`** - Complete API reference
  - All endpoints organized by role
  - Request/response examples for each endpoint
  - Error response formats
  - Authentication headers
  - curl testing examples

## Key Features

### 1. Role Enforcement
- Only Admin and Customer roles allowed
- Roles are stored in database
- Roles are verified on every protected request
- Cannot be changed through API for security

### 2. Customer Registration
- Public registration endpoint creates customer accounts only
- Admin accounts cannot be created via API
- Admin users must be created through database initialization script

### 3. JWT Authentication
- Tokens include user ID and role
- Tokens expire after configured interval
- Tokens are verified on every protected request
- Both header and cookie authentication supported

### 4. Permission System
- Each role has specific permissions
- Permissions are mapped to API endpoints
- Admin has all permissions
- Customers have limited shopping-related permissions

### 5. Account Management
- Passwords are hashed with bcrypt
- User accounts can be enabled/disabled
- Admin can disable customer accounts
- Users can change their own passwords

### 6. Security Features
- No privilege escalation possible
- Role cannot be changed through API
- Disabled accounts cannot login
- Passwords have minimum length requirement
- All admin actions can be logged

## File Structure

```
inventory_system/
├── app/
│   ├── api/
│   │   ├── auth.py (updated)
│   │   ├── products.py (enhanced)
│   │   ├── categories.py (enhanced)
│   │   ├── suppliers.py (enhanced)
│   │   ├── customers.py (new)
│   │   ├── carts.py (new)
│   │   ├── orders.py (enhanced)
│   │   ├── wishlists.py (new)
│   │   ├── invoices.py (enhanced)
│   │   ├── notifications.py (enhanced)
│   │   ├── backup.py (enhanced)
│   │   └── settings.py (enhanced)
│   ├── core/
│   │   ├── roles.py (new)
│   │   ├── dependencies.py (enhanced)
│   │   └── auth.py (existing)
│   ├── models/
│   │   └── user.py (enhanced)
│   ├── repositories/
│   │   └── base_repository.py (fixed)
│   ├── schemas/
│   │   └── user.py (updated)
│   └── services/
│       └── user_service.py (enhanced)
├── init_db.py (new)
├── RBAC_IMPLEMENTATION.md (new)
└── API_ENDPOINTS.md (new)
```

## Usage Instructions

### 1. Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Create Admin and Customer roles
- Prompt you to create an admin user (first time only)

### 2. Start the Application

```bash
uvicorn app.main:app --reload
```

### 3. Register as Customer

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123",
    "full_name": "John Doe"
  }'
```

### 4. Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=secure_password_123"
```

### 5. Use Access Token

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer {access_token}"
```

## Database Schema

### Roles Table
```
roles (new, required)
├── id (INTEGER, PRIMARY KEY)
├── name (VARCHAR(50), UNIQUE, NOT NULL)
└── users (relationship)
```

### Users Table (Enhanced)
```
users
├── id (INTEGER, PRIMARY KEY)
├── username (VARCHAR(50), UNIQUE, NOT NULL)
├── email (VARCHAR(100), UNIQUE, NOT NULL)
├── hashed_password (VARCHAR(255), NOT NULL)
├── full_name (VARCHAR(100))
├── is_active (BOOLEAN, DEFAULT True)
├── role_id (INTEGER, FOREIGN KEY to roles.id, NOT NULL) ← ENHANCED
├── created_at (DATETIME)
└── updated_at (DATETIME)
```

## Testing

### Admin Access
1. Create admin user during init_db.py
2. Login with admin credentials
3. Try accessing `/api/products/` (should work for all)
4. Try accessing `POST /api/products/` (admin only, should work)
5. Try accessing `DELETE /api/products/1` (admin only, should work)

### Customer Access
1. Register as customer
2. Login with customer credentials
3. Try accessing `/api/products/` (should work)
4. Try accessing `POST /api/products/` (should get 403 Forbidden)
5. Try accessing `/api/carts/` (should work)

### Unauthenticated Access
1. Try accessing `/api/auth/me` without token (should get 401 Unauthorized)
2. Try accessing `/api/products/` without token (should work - public)
3. Try accessing `POST /api/products/` without token (should get 401 Unauthorized)

## Security Checklist

✅ Only two roles allowed (Admin and Customer)
✅ No privilege escalation possible
✅ Role cannot be changed through API
✅ Passwords hashed with bcrypt
✅ JWT tokens include role information
✅ Tokens expire after configured interval
✅ All protected endpoints check role
✅ Account enable/disable functionality
✅ Password change endpoint available
✅ Profile update endpoint available
✅ Admin actions are auditable
✅ Customer accounts cannot access admin features
✅ Admin accounts cannot be created via registration

## Customization

### Add New Admin
Edit in Python and run:
```python
from app.database import SessionLocal
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

db = SessionLocal()
repo = UserRepository(db)
service = UserService(repo)

admin = service.create_admin(
    username="admin2",
    email="admin2@example.com",
    password="secure_password",
    full_name="Admin Two"
)
db.close()
```

### Modify Permissions
Edit `app/core/roles.py` to add/remove permissions for each role.

### Add New Role (Future)
Update `app/core/roles.py` to add new role enum and permissions mapping.

## Troubleshooting

### Issue: "Admin access required"
- User is logged in as customer
- Switch to admin account or check user role

### Issue: "Not authenticated"
- No JWT token provided
- Token is expired
- Login again to get new token

### Issue: Database error during init_db.py
- Database already exists
- Delete database and try again
- Or manually create roles in database

### Issue: Cannot create admin user
- Admin users must be created through init_db.py
- Or directly in database
- API registration is customer-only

## Next Steps

1. ✅ Implement role-based access control - DONE
2. Run `python init_db.py` to initialize database
3. Test all endpoints with both admin and customer accounts
4. Deploy to production with HTTPS
5. Monitor logs for unauthorized access attempts
6. Regularly backup database
7. Update admin password after first login

## Support

For detailed documentation:
- See `RBAC_IMPLEMENTATION.md` for RBAC documentation
- See `API_ENDPOINTS.md` for API reference
- Check `app/core/roles.py` for permission definitions
- Review `app/core/dependencies.py` for role dependencies
