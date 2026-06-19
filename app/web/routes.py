from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.templates import templates
from app.core.auth import get_current_user_optional, get_current_user, create_access_token
from app.core.dependencies import require_admin, require_authenticated
from app.models.user import User
from app.database import get_db
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.config import settings  # <-- added import

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    # Prepare basic dashboard totals (safe if no data)
    totals = {
        "products": db.query("products").count() if False else None
    }
    try:
        products_count = db.query("products").count()
    except Exception:
        # Fallback using model
        from app.models.product import Product
        products_count = db.query(Product).count()

    try:
        from app.models.order import Order
        orders_count = db.query(Order).count()
        revenue = db.query(func.coalesce(func.sum(Order.total_amount), 0.0)).scalar()
    except Exception:
        orders_count = 0
        revenue = 0.0

    try:
        from app.models.user import User
        customers_count = db.query(User).filter(User.role.has(name='customer')).count()
    except Exception:
        customers_count = db.query(User).count() if current_user else 0

    # Recent orders
    recent_orders = []
    try:
        from app.models.order import Order
        recent = db.query(Order).order_by(Order.created_at.desc()).limit(6).all()
        for o in recent:
            recent_orders.append({
                "id": o.order_number or o.id,
                "customer_name": getattr(o.customer, 'full_name', 'Guest'),
                "status": getattr(o.status, 'value', str(o.status)),
                "total": f"{o.total_amount:.2f}"
            })
    except Exception:
        recent_orders = []

    totals = {"products": products_count, "orders": orders_count, "revenue": f"{revenue:.2f}", "customers": customers_count}

    # If not authenticated, redirect to login (hide dashboard)
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request, "user": current_user, "totals": totals, "recent_orders": recent_orders})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # Pass explicit user=None so templates can conditionally hide sidebar
    return templates.TemplateResponse("login.html", {"request": request, "user": None})

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("username")
    password = form.get("password")
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.authenticate(email, password)
    if not user:
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid email or password"}
        )
    token = create_access_token(data={"sub": str(user.id), "role": user.role.name})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        secure=False,  # set to True if using HTTPS
        samesite="lax"
    )
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "user": None})

@router.get("/products", response_class=HTMLResponse)
async def products_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("products.html", {"request": request, "user": current_user})

# --- Add guarded pages to avoid 404s and enforce RBAC ---
@router.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("categories.html", {"request": request, "user": current_user})

@router.get("/warehouses", response_class=HTMLResponse)
async def warehouses_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Warehouses"})

@router.get("/suppliers", response_class=HTMLResponse)
async def suppliers_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Suppliers"})

@router.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Orders"})

@router.get("/customers", response_class=HTMLResponse)
async def customers_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Customers"})

@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Reports"})

@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Analytics"})

@router.get("/notifications", response_class=HTMLResponse)
async def notifications_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Notifications"})

@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("placeholder.html", {"request": request, "user": current_user, "title": "Settings"})

# Add more pages as needed

# Additional web pages to avoid 404s
@router.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("cart.html", {"request": request, "user": current_user})


@router.get("/wishlists", response_class=HTMLResponse)
async def wishlists_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("wishlists.html", {"request": request, "user": current_user})


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})


@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("users.html", {"request": request, "user": current_user})


@router.get("/backup", response_class=HTMLResponse)
async def backup_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("backup.html", {"request": request, "user": current_user})


@router.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    if not current_user.role or current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("logs.html", {"request": request, "user": current_user})


@router.get("/order-success", response_class=HTMLResponse)
async def order_success_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("order_success.html", {"request": request, "user": current_user})