from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User

router = APIRouter()

# ========== ADMIN ENDPOINTS ONLY ==========

@router.get("/")
def get_all_settings(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all settings (admin only)."""
    # TODO: Implement get settings
    return {
        "company_name": "My Company",
        "currency": "USD",
        "tax_rate": 10,
        "email_smtp": "smtp.example.com",
        "theme": "light"
    }

@router.get("/{setting_key}")
def get_setting(
    setting_key: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get specific setting (admin only)."""
    # TODO: Implement get setting
    return {"key": setting_key, "value": ""}

@router.put("/{setting_key}")
def update_setting(
    setting_key: str,
    value: Any,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update setting (admin only)."""
    # TODO: Implement update setting
    return {"message": "Setting updated", "key": setting_key, "value": value}

@router.post("/company-info")
def update_company_info(
    company_name: str = None,
    logo_url: str = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update company information (admin only)."""
    # TODO: Implement company info update
    return {"message": "Company info updated"}

@router.post("/currency")
def update_currency(
    currency: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update currency setting (admin only)."""
    # TODO: Implement currency update
    return {"message": "Currency updated", "currency": currency}

@router.post("/tax")
def update_tax_settings(
    tax_rate: float,
    tax_type: str = "percentage",
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update tax settings (admin only)."""
    # TODO: Implement tax settings update
    return {"message": "Tax settings updated", "rate": tax_rate, "type": tax_type}

@router.post("/email")
def update_email_settings(
    smtp_server: str,
    smtp_port: int,
    email_address: str,
    password: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update email settings (admin only)."""
    # TODO: Implement email settings update
    return {"message": "Email settings updated"}

@router.post("/theme")
def update_theme_settings(
    theme: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update theme settings (admin only)."""
    # TODO: Implement theme settings update
    return {"message": "Theme updated", "theme": theme}
