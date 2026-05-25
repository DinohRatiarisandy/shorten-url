from fastapi import APIRouter, Depends, HTTPException
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


@router.get(
    "/admin/links/id/{id}",
    response_model=schemas.LinkResponse,
    description="Get link by his id",
)
def get_link_by_id(
    id: str, db: Session = Depends(get_db), user=Depends(get_current_admin_user)
):
    selected_link = db.query(models.Link).filter(models.Link.id == id).first()

    if selected_link:
        return selected_link

    raise HTTPException(status_code=404, detail="Link not found")
