import os
from urllib.parse import urlparse

import dotenv
from fastapi import HTTPException
from hashids import Hashids
from sqlalchemy.orm import Session

import models
import schemas

dotenv.load_dotenv(".env", override=True)
hashids_salt_key = os.getenv("HASHID_SALT_SECRET")
hashids = Hashids(salt=hashids_salt_key or "dinoh-liantsoa-ratiarisandy", min_length=5)


def is_valid_url(url: str) -> bool:
    """Vérifie si une URL est valide (format de base)."""
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except Exception:
        return False


def generate_short_code(next_id: int) -> str:
    """Génère un code court unique à partir d'un ID."""
    return hashids.encode(next_id)


def get_existing_link_by_url(db: Session, url: str) -> models.Link | None:
    """Retourne le lien existant pour une URL, ou None si introuvable."""
    return db.query(models.Link).filter(models.Link.original_url == url).first()


def create_link(db: Session, link: schemas.LinkCreate):
    if not is_valid_url(link.original_url):
        raise HTTPException(
            status_code=400, detail="Invalid URL. Must start with http:// or https://"
        )

    existing_link = get_existing_link_by_url(db, link.original_url)

    if existing_link:
        return existing_link

    next_id = get_next_id(db)
    short_code = generate_short_code(next_id)
    db_link = models.Link(original_url=link.original_url, short_code=short_code)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_link_by_short_code(db: Session, short_code: str):
    return db.query(models.Link).filter(models.Link.short_code == short_code).first()


def get_next_id(db: Session) -> int:
    """Récupère le prochain ID disponible."""
    last_id = db.query(models.Link.id).order_by(models.Link.id.desc()).limit(1).scalar()
    return (last_id + 1) if last_id else 1
