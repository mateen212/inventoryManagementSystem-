from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.dependencies import require_admin, require_authenticated
from app.models.user import User
from app.models.notification import Notification
from app.models.user import User as UserModel
from sqlalchemy import or_

router = APIRouter()

# ========== CUSTOMER ENDPOINTS (Own notifications only) ==========

@router.get("/")
def get_notifications(
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Get notifications for current user."""
    q = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    items = []
    for n in q:
        items.append({"id": n.id, "title": n.title, "message": n.message, "is_read": n.is_read, "created_at": n.created_at})
    return {"user_id": current_user.id, "notifications": items}

@router.put("/{notification_id}/mark-read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Mark notification as read."""
    n = db.query(Notification).filter(Notification.id == notification_id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    if n.user_id != current_user.id and (not current_user.role or current_user.role.name != 'admin'):
        raise HTTPException(status_code=403, detail="Not allowed")
    n.is_read = True
    db.add(n)
    db.commit()
    return {"message": "Notification marked as read", "notification_id": notification_id}

# ========== ADMIN ENDPOINTS ==========

@router.post("/send")
def send_notification(
    user_id: int,
    title: str,
    message: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Send notification to user (admin only)."""
    u = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    n = Notification(user_id=user_id, title=title, message=message)
    db.add(n)
    db.commit()
    return {"message": "Notification sent", "user_id": user_id}

@router.post("/broadcast")
def broadcast_notification(
    title: str,
    message: str,
    target_role: str = "customer",
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Broadcast notification to all users of a role (admin only)."""
    # find users by role name
    users = db.query(UserModel).filter(UserModel.role.has(name=target_role)).all()
    for u in users:
        n = Notification(user_id=u.id, title=title, message=message)
        db.add(n)
    db.commit()
    return {"message": f"Notification broadcasted to {target_role}s", "count": len(users)}
