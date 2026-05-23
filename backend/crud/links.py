from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from services.shortener import generate_unique_code
from services.validators import is_valid_url


def get_existing_link_by_url(db: Session, url: str) -> models.Link | None:
    """Retourne le lien existant pour une URL, ou None si introuvable."""
    return db.query(models.Link).filter(models.Link.original_url == url).first()


def create_link(db: Session, link: schemas.LinkCreate):
    if not is_valid_url(link.original_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    existing = get_existing_link_by_url(db, link.original_url)
    if existing:
        return existing

    # Si un custom code est fourni
    if link.custom_short_code:
        code = generate_unique_code(
            db, lenght=0, custom_short_code=link.custom_short_code
        )
    else:
        code = generate_unique_code(db)

    db_link = models.Link(original_url=link.original_url, short_code=code)

    db.add(db_link)
    db.commit()
    db.refresh(db_link)

    return db_link


def get_link_by_short_code(db: Session, short_code: str):
    return db.query(models.Link).filter(models.Link.short_code == short_code).first()
