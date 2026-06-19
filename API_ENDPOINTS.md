# API Endpoints Reference by Role

## Authentication Endpoints

### Public Endpoints (No Authentication Required)

#### Register New Customer
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "full_name": "John Doe"
}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "role_id": 2,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secure_password_123

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Authenticated Endpoints

#### Get Current User Profile
```
GET /api/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "role_id": 2,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Logout
```
POST /api/auth/logout
Authorization: Bearer {access_token}

Response: 200 OK
{
  "message": "Successfully logged out"
}
```

#### Change Password
```
POST /api/auth/change-password
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "current_password_123",
  "new_password": "new_password_456"
}

Response: 200 OK
{
  "message": "Password changed successfully"
}
```

#### Update Profile
```
POST /api/auth/update-profile
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "full_name": "John Doe Smith",
  "username": "john_doe_smith"
}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe_smith",
  "email": "john@example.com",
  "full_name": "John Doe Smith",
  "is_active": true,
  "role_id": 2,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

---

## Product Endpoints

### Public Endpoints (No Authentication)

#### List All Products
```
GET /api/products/?skip=0&limit=100

Response: 200 OK
[
  {
    "id": 1,
    "name": "Product 1",
    "price": 99.99,
    "stock": 100,
    "category_id": 1
  },
  ...
]
```

#### Search Products
```
GET /api/products/search?q=laptop

Response: 200 OK
[
  {
    "id": 2,
    "name": "Dell Laptop",
    "price": 899.99,
    "stock": 5,
    "category_id": 3
  },
  ...
]
```

#### Get Product Details
```
GET /api/products/{product_id}

Response: 200 OK
{
  "id": 1,
  "name": "Product 1",
  "description": "Product description",
  "price": 99.99,
  "stock": 100,
  "category_id": 1,
  "supplier_id": 1
}
```

### Admin-Only Endpoints

#### Create Product
```
POST /api/products/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "New Product",
  "description": "Product description",
  "price": 149.99,
  "stock": 50,
  "category_id": 1,
  "supplier_id": 1,
  "sku": "PROD-001"
}

Response: 201 Created
{
  "id": 3,
  "name": "New Product",
  "price": 149.99,
  "stock": 50,
  "category_id": 1
}
```

#### Update Product
```
PUT /api/products/{product_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Updated Product",
  "price": 199.99,
  "stock": 75
}

Response: 200 OK
{
  "id": 3,
  "name": "Updated Product",
  "price": 199.99,
  "stock": 75,
  "category_id": 1
}
```

#### Delete Product
```
DELETE /api/products/{product_id}
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "detail": "Product deleted successfully"
}
```

#### Upload Product Images
```
POST /api/products/{product_id}/upload-images
Authorization: Bearer {admin_token}
Content-Type: multipart/form-data

files: [image1.jpg, image2.jpg, image3.jpg]

Response: 200 OK
{
  "detail": "Uploaded 3 images",
  "product_id": 1
}
```

#### Generate Product Barcode
```
POST /api/products/{product_id}/generate-barcode
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "detail": "Barcode generated",
  "product_id": 1,
  "barcode": "123456789"
}
```

#### Generate QR Code
```
POST /api/products/{product_id}/generate-qrcode
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "detail": "QR code generated",
  "product_id": 1,
  "qrcode_url": "/static/qrcodes/product_1.png"
}
```

#### Manage Stock
```
POST /api/products/{product_id}/manage-stock?quantity=10&action=add
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "detail": "Stock add completed",
  "product_id": 1,
  "new_quantity": 110
}
```

---

## Category Endpoints

### Public Endpoints

#### List Categories
```
GET /api/categories/?skip=0&limit=100

Response: 200 OK
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices"
  },
  ...
]
```

### Admin-Only Endpoints

#### Create Category
```
POST /api/categories/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Clothing",
  "description": "Apparel and accessories"
}

Response: 201 Created
{
  "id": 3,
  "name": "Clothing",
  "description": "Apparel and accessories"
}
```

#### Update Category
```
PUT /api/categories/{category_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Clothing & Accessories",
  "description": "Updated description"
}

Response: 200 OK
{
  "id": 3,
  "name": "Clothing & Accessories"
}
```

#### Delete Category
```
DELETE /api/categories/{category_id}
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "detail": "Category deleted successfully"
}
```

---

## Cart Endpoints

### Customer Endpoints

#### Get Cart
```
GET /api/carts/
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "product_name": "Product 1",
      "quantity": 2,
      "price": 99.99
    }
  ]
}
```

#### Add to Cart
```
POST /api/carts/add?product_id=1&quantity=2
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Product added to cart",
  "product_id": 1,
  "quantity": 2
}
```

#### Update Cart Item
```
PUT /api/carts/{item_id}?quantity=5
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Cart item updated",
  "item_id": 1,
  "quantity": 5
}
```

#### Remove from Cart
```
DELETE /api/carts/{item_id}
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Item removed from cart"
}
```

#### Checkout
```
POST /api/carts/checkout
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Order created",
  "order_id": 1
}
```

---

## Order Endpoints

### Customer Endpoints

#### Create Order
```
POST /api/orders/
Authorization: Bearer {customer_token}

Response: 201 Created
{
  "message": "Order created successfully",
  "order_id": 1
}
```

#### Get My Orders
```
GET /api/orders/my-orders?skip=0&limit=10
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "user_id": 1,
  "orders": [
    {
      "id": 1,
      "total": 299.97,
      "status": "pending",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

#### Get Order Details
```
GET /api/orders/{order_id}
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "order_id": 1,
  "details": {
    "user_id": 1,
    "total": 299.97,
    "status": "pending",
    "items": []
  }
}
```

#### Cancel Order
```
POST /api/orders/{order_id}/cancel
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Order cancelled successfully",
  "order_id": 1
}
```

#### Download Invoice
```
GET /api/orders/{order_id}/invoice/download
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Invoice download initiated",
  "order_id": 1
}
```

### Admin Endpoints

#### List All Orders
```
GET /api/orders/admin/all?skip=0&limit=100
Authorization: Bearer {admin_token}

Response: 200 OK
[
  {
    "id": 1,
    "customer_id": 1,
    "total": 299.97,
    "status": "pending"
  }
]
```

#### Update Order Status
```
PUT /api/orders/{order_id}/status?status=shipped
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "message": "Order status updated",
  "order_id": 1,
  "new_status": "shipped"
}
```

#### Cancel Order (Admin)
```
POST /api/orders/{order_id}/admin-cancel
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "reason": "Out of stock"
}

Response: 200 OK
{
  "message": "Order cancelled by admin",
  "order_id": 1,
  "reason": "Out of stock"
}
```

#### Print Invoice
```
POST /api/orders/{order_id}/print-invoice
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "message": "Invoice sent to printer",
  "order_id": 1
}
```

---

## Wishlist Endpoints

### Customer Endpoints

#### Get Wishlist
```
GET /api/wishlists/
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "user_id": 1,
  "items": [
    {
      "product_id": 5,
      "product_name": "Product 5"
    }
  ]
}
```

#### Add to Wishlist
```
POST /api/wishlists/add?product_id=5
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Product added to wishlist",
  "product_id": 5
}
```

#### Remove from Wishlist
```
DELETE /api/wishlists/{item_id}
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Item removed from wishlist"
}
```

#### Move to Cart
```
POST /api/wishlists/{item_id}/move-to-cart
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Item moved to cart"
}
```

---

## Notification Endpoints

### Customer Endpoints

#### Get Notifications
```
GET /api/notifications/
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "user_id": 1,
  "notifications": [
    {
      "id": 1,
      "title": "Order Shipped",
      "message": "Your order has been shipped",
      "read": false
    }
  ]
}
```

#### Mark as Read
```
PUT /api/notifications/{notification_id}/mark-read
Authorization: Bearer {customer_token}

Response: 200 OK
{
  "message": "Notification marked as read",
  "notification_id": 1
}
```

### Admin Endpoints

#### Send Notification
```
POST /api/notifications/send
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "user_id": 1,
  "title": "Special Offer",
  "message": "Get 20% off on electronics"
}

Response: 200 OK
{
  "message": "Notification sent",
  "user_id": 1
}
```

#### Broadcast Notification
```
POST /api/notifications/broadcast
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "title": "Maintenance Alert",
  "message": "System maintenance scheduled",
  "target_role": "customer"
}

Response: 200 OK
{
  "message": "Notification broadcasted to customers"
}
```

---

## Customer Management Endpoints

### Admin-Only Endpoints

#### List All Customers
```
GET /api/customers/?skip=0&limit=100
Authorization: Bearer {admin_token}

Response: 200 OK
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "role_id": 2
  }
]
```

#### Search Customers
```
GET /api/customers/search?q=john
Authorization: Bearer {admin_token}

Response: 200 OK
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
]
```

#### Get Customer Details
```
GET /api/customers/{customer_id}
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Update Customer
```
PUT /api/customers/{customer_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "full_name": "John D Smith",
  "email": "john.smith@example.com"
}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john.smith@example.com",
  "full_name": "John D Smith"
}
```

#### Disable Customer
```
POST /api/customers/{customer_id}/disable
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "message": "Customer account disabled"
}
```

#### Enable Customer
```
POST /api/customers/{customer_id}/enable
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "message": "Customer account enabled"
}
```

---

## Supplier Endpoints

### Admin-Only Endpoints

#### List Suppliers
```
GET /api/suppliers/?skip=0&limit=100
Authorization: Bearer {admin_token}

Response: 200 OK
[
  {
    "id": 1,
    "name": "Supplier 1",
    "contact_person": "John Supplier",
    "email": "john@supplier.com"
  }
]
```

#### Create Supplier
```
POST /api/suppliers/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "New Supplier",
  "contact_person": "Jane Supplier",
  "email": "jane@supplier.com",
  "phone": "+1234567890",
  "address": "123 Supplier St"
}

Response: 201 Created
{
  "id": 2,
  "name": "New Supplier"
}
```

#### Update Supplier
```
PUT /api/suppliers/{supplier_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Updated Supplier",
  "contact_person": "Jane Supplier"
}

Response: 200 OK
{
  "id": 2,
  "name": "Updated Supplier"
}
```

#### Delete Supplier
```
DELETE /api/suppliers/{supplier_id}
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "detail": "Supplier deleted successfully"
}
```

---

## Settings Endpoints

### Admin-Only Endpoints

#### Get All Settings
```
GET /api/settings/
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "company_name": "My Inventory Store",
  "currency": "USD",
  "tax_rate": 10,
  "email_smtp": "smtp.gmail.com",
  "theme": "light"
}
```

#### Get Specific Setting
```
GET /api/settings/{setting_key}
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "key": "company_name",
  "value": "My Inventory Store"
}
```

#### Update Setting
```
PUT /api/settings/{setting_key}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "value": "New Company Name"
}

Response: 200 OK
{
  "message": "Setting updated",
  "key": "company_name",
  "value": "New Company Name"
}
```

#### Update Company Info
```
POST /api/settings/company-info
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "company_name": "Updated Company",
  "logo_url": "https://example.com/logo.png"
}

Response: 200 OK
{
  "message": "Company info updated"
}
```

#### Update Currency
```
POST /api/settings/currency
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "currency": "EUR"
}

Response: 200 OK
{
  "message": "Currency updated",
  "currency": "EUR"
}
```

#### Update Tax Settings
```
POST /api/settings/tax
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "tax_rate": 15,
  "tax_type": "percentage"
}

Response: 200 OK
{
  "message": "Tax settings updated",
  "rate": 15,
  "type": "percentage"
}
```

#### Update Email Settings
```
POST /api/settings/email
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "email_address": "noreply@example.com",
  "password": "secure_password"
}

Response: 200 OK
{
  "message": "Email settings updated"
}
```

#### Update Theme
```
POST /api/settings/theme
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "theme": "dark"
}

Response: 200 OK
{
  "message": "Theme updated",
  "theme": "dark"
}
```

---

## Backup Endpoints

### Admin-Only Endpoints

#### Get Backup History
```
GET /api/backup/history?skip=0&limit=50
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "backups": [
    {
      "id": 1,
      "created_at": "2024-01-15T10:30:00",
      "description": "Daily backup",
      "size": "102.5 MB"
    }
  ]
}
```

#### Create Backup
```
POST /api/backup/create
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "description": "Pre-sale backup"
}

Response: 200 OK
{
  "message": "Backup created successfully",
  "backup_id": 5,
  "description": "Pre-sale backup"
}
```

#### Restore Backup
```
POST /api/backup/{backup_id}/restore
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "message": "Backup restoration initiated",
  "backup_id": 5
}
```

#### Delete Backup
```
DELETE /api/backup/{backup_id}
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "message": "Backup deleted successfully",
  "backup_id": 5
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "Product not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

---

## Headers Required

All authenticated requests must include:

```
Authorization: Bearer {access_token}
Content-Type: application/json (for POST, PUT requests)
```

## Testing

Use the provided test examples with curl:

```bash
# Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123","full_name":"John Doe"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=password123"

# Get products with token
curl -X GET "http://localhost:8000/api/products/" \
  -H "Authorization: Bearer {token}"
```
