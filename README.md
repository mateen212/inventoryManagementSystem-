# Inventory Management System

A production-ready inventory management web application built with FastAPI, SQLAlchemy, and Bootstrap 5.

## Features

- Admin and Customer roles
- Product, Category, Warehouse, Supplier, Customer management
- Order management with statuses
- Shopping cart
- Reports and analytics
- Barcode and QR code generation
- Import/Export (CSV, Excel, JSON, PDF)
- Notification center
- Invoice generation
- Image management
- Backup and restore
- Wishlist
- Activity logs
- Dark/Light mode

## Installation

1. Create a virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\\Scripts\\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and update settings.
5. Run migrations: `alembic upgrade head`
6. Run the application: `inventory-manager run` or `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Usage

- Access the web interface at `http://localhost:8000`
- Admin login: admin@example.com / admin123 (seed)

## CLI Commands

- `inventory-manager run` - start the server
- `inventory-manager add-product` - add a product via CLI
- `inventory-manager update-stock` - update stock
- `inventory-manager export-data` - export data
- `inventory-manager backup-db` - backup database
- `inventory-manager restore-db` - restore database

## Testing

Run tests: `pytest --cov=app`

## License

MIT
