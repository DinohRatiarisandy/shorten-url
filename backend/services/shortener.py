import os
import random
import string

import dotenv

import models

dotenv.load_dotenv(override=True)

ALPHABET = os.getenv("BASE62_ALPHABET", string.ascii_letters + string.digits)
CODE_LENGTH = 5


def generate_code(length=CODE_LENGTH):
    return "".join(random.choices(ALPHABET, k=length))


def generate_unique_code(db):
    tries = 0
    while True:
        if tries >= 3:
            code = generate_code(6)
        else:
            code = generate_code()

        exists = db.query(models.Link).filter_by(short_code=code).first()

        if not exists:
            return code

        tries += 1
