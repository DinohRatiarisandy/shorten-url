from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import models
from auth.security import decode_access_token
from database import get_db

router = APIRouter(tags=["Auth"])


@router.get("/auth/me")
def get_me(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_access_token(access_token)

    user = db.query(models.User).filter(models.User.id == payload["sub"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }


# logout
@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="acces_token", path="/")
    return {"message": "Logged out"}
