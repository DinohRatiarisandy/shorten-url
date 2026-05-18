import random
import string

from sqlalchemy.orm import Session

import models
import schemas


def generate_short_code(length: int = 6) -> str:
    """Génère un code court aléatoire (ex: 'aBc123')"""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def create_link(db: Session, link: schemas.LinkCreate):
    short_code = generate_short_code()
    db_link = models.Link(original_url=link.original_url, short_code=short_code)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_link_by_short_code(db: Session, short_code: str):
    return db.query(models.Link).filter(models.Link.short_code == short_code).first()
