import os

import dotenv
from hashids import Hashids
from sqlalchemy.orm import Session

import models
import schemas

dotenv.load_dotenv(".env", override=True)
hashids_salt_key = os.getenv("HASHID_SALT_SECRET")
hashids = Hashids(salt=hashids_salt_key or "dinoh-liantsoa-ratiarisandy", min_length=6)


def generate_short_code(next_id: int) -> str:
    """Génère un code court unique à partir d'un ID."""
    return hashids.encode(next_id)


def create_link(db: Session, link: schemas.LinkCreate):
    last_link = db.query(models.Link).order_by(models.Link.id.desc()).limit(1).scalar()
    next_id = (last_link.id + 1) if last_link else 1
    short_code = generate_short_code(next_id)
    db_link = models.Link(original_url=link.original_url, short_code=short_code)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_link_by_short_code(db: Session, short_code: str):
    return db.query(models.Link).filter(models.Link.short_code == short_code).first()
