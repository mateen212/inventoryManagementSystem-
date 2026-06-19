"""
Role definitions and permissions for the inventory system.
"""
from enum import Enum
from typing import Set

class UserRole(str, Enum):
    """Allowed user roles in the system."""
    ADMIN = "admin"
    CUSTOMER = "customer"

# Define which permissions each role has
ADMIN_PERMISSIONS: Set[str] = {
    # Authentication
    "auth:login",
    "auth:logout",
    "auth:change_password",
    "auth:update_profile",
    
    # Products
    "product:create",
    "product:read",
    "product:update",
    "product:delete",
    "product:upload_images",
    "product:generate_barcode",
    "product:generate_qrcode",
    "product:manage_stock",
    
    # Categories
    "category:create",
    "category:read",
    "category:update",
    "category:delete",
    
    # Warehouses
    "warehouse:create",
    "warehouse:read",
    "warehouse:update",
    "warehouse:delete",
    "warehouse:transfer_inventory",
    
    # Suppliers
    "supplier:create",
    "supplier:read",
    "supplier:update",
    "supplier:delete",
    
    # Customers
    "customer:read",
    "customer:search",
    "customer:update",
    "customer:disable",
    
    # Orders
    "order:read_all",
    "order:update_status",
    "order:cancel",
    "order:print_invoice",
    
    # Notifications
    "notification:send",
    "notification:read",
    
    # Reports
    "report:sales",
    "report:inventory",
    "report:revenue",
    "report:profit",
    "report:export",
    
    # Analytics
    "analytics:view",
    "analytics:monthly_sales",
    "analytics:top_products",
    "analytics:revenue",
    "analytics:inventory_value",
    
    # Settings
    "settings:read",
    "settings:update",
    "settings:company",
    "settings:currency",
    "settings:tax",
    "settings:email",
    "settings:theme",
    
    # Users
    "user:read",
    "user:activate",
    "user:suspend",
    
    # Backup
    "backup:create",
    "backup:restore",
    "backup:read_history",
    
    # Logs
    "log:activity",
    "log:error",
    
    # Import/Export
    "import_export:csv",
    "import_export:excel",
    "import_export:json",
    "import_export:pdf",
}

CUSTOMER_PERMISSIONS: Set[str] = {
    # Authentication
    "auth:register",
    "auth:login",
    "auth:logout",
    "auth:reset_password",
    "auth:update_profile",
    
    # Products
    "product:read",
    "product:search",
    "product:filter",
    
    # Cart
    "cart:add",
    "cart:remove",
    "cart:update_quantity",
    
    # Wishlist
    "wishlist:add",
    "wishlist:remove",
    "wishlist:move_to_cart",
    
    # Orders
    "order:create",
    "order:cancel_pending",
    "order:read_own",
    "order:download_invoice",
    
    # Notifications
    "notification:read",
    "notification:mark_read",
    
    # Profile
    "profile:update",
    "profile:change_password",
    
    # Dashboard
    "dashboard:view_own_orders",
    "dashboard:view_recent_purchases",
    "dashboard:view_notifications",
}

# Map roles to their permissions
ROLE_PERMISSIONS = {
    UserRole.ADMIN: ADMIN_PERMISSIONS,
    UserRole.CUSTOMER: CUSTOMER_PERMISSIONS,
}

def has_permission(role: UserRole, permission: str) -> bool:
    """Check if a role has a specific permission."""
    return permission in ROLE_PERMISSIONS.get(role, set())

def has_any_permission(role: UserRole, permissions: Set[str]) -> bool:
    """Check if a role has any of the specified permissions."""
    role_perms = ROLE_PERMISSIONS.get(role, set())
    return any(perm in role_perms for perm in permissions)

def has_all_permissions(role: UserRole, permissions: Set[str]) -> bool:
    """Check if a role has all of the specified permissions."""
    role_perms = ROLE_PERMISSIONS.get(role, set())
    return all(perm in role_perms for perm in permissions)
