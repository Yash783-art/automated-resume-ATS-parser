from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User

def get_current_user(
    x_clerk_id: str = Header(..., alias="X-Clerk-User-Id"),
    db: Session = Depends(get_db)
) -> User:
    """
    Simplified auth dependency. In production, this would verify a JWT.
    For now, it expects the Clerk User ID in a header.
    """
    user = db.query(User).filter(User.clerk_id == x_clerk_id).first()
    if not user:
        # Auto-create user if they don't exist in our DB yet
        # email is optional in the model, so we can omit it here
        user = User(clerk_id=x_clerk_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
