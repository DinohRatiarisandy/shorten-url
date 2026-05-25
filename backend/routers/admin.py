from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from auth.dependencies import get_current_admin_user
from database import get_db

router = APIRouter(tags=["Admin"])


@router.get("/admin/links", response_model=list[schemas.LinkResponse])
def get_links(db: Session = Depends(get_db), user=Depends(get_current_admin_user)):
    all_links = db.query(models.Link).all()
    return all_links
