from fastapi import Cookie, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import models
from auth.security import decode_access_token
from database import get_db

security = HTTPBearer()


def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db),
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_access_token(access_token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_admin_user(current_user=Depends(get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin only")

    return current_user
