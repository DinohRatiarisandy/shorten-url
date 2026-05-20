import os

import dotenv

dotenv.load_dotenv(override=True)

ALPHABET = os.getenv(
    "BASE62_ALPHABET", "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

SECRET = int(os.getenv("SHORTENER_SECRET", 987654321))

MIN_LENGTH = 5


def encode_base62(num):
    if num == 0:
        return ALPHABET[0]

    result = ""

    while num > 0:
        num, remainder = divmod(num, 62)

        result = ALPHABET[remainder] + result

    return result


def generate_short_code(id):
    mixed = id ^ SECRET

    code = encode_base62(mixed)

    return code.rjust(MIN_LENGTH, ALPHABET[0])
