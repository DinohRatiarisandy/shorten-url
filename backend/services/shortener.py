import os
import random
import string

import dotenv
from sqlalchemy.orm import Session

import models

dotenv.load_dotenv(override=True)

ALPHABET = os.getenv("BASE62_ALPHABET", string.ascii_letters + string.digits)


def generate_code(length=5):
    return "".join(random.choices(ALPHABET, k=length))


def generate_unique_code(db: Session, lenght=5, custom_short_code: str | None = None):
    call_nb = 0
    while True:
        if call_nb > 10:
            lenght += 1
            code = (
                custom_short_code + "-" if custom_short_code else ""
            ) + generate_code(lenght)
            call_nb = 0
        else:
            code = (custom_short_code or "") + generate_code(lenght)
            call_nb += 1

        exists = db.query(models.Link).filter_by(short_code=code).first()

        if not exists:
            return code
