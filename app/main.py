import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.api import auth, products, categories, suppliers, customers, orders, carts, invoices, wishlists, notifications, backup, settings as settings_router
from app.web import routes as web_routes
from app.core.templates import templates
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(suppliers.router, prefix="/api/suppliers", tags=["suppliers"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(carts.router, prefix="/api/carts", tags=["carts"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(wishlists.router, prefix="/api/wishlists", tags=["wishlists"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(backup.router, prefix="/api/backup", tags=["backup"])
app.include_router(settings_router.router, prefix="/api/settings", tags=["settings"])

# Include web routes
app.include_router(web_routes.router)

@app.on_event("startup")
def startup():
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed admin
    from app.services.user_service import UserService
    from app.repositories.user_repository import UserRepository
    from app.database import SessionLocal
    db = SessionLocal()
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    admin = user_service.get_by_email("admin@example.com")
    if not admin:
        user_service.create_admin("Admin", "admin@example.com", "admin123")
    db.close()
    logger.info("Application started")
