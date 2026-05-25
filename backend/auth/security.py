import os
from datetime import UTC, datetime, timedelta

import bcrypt
import dotenv
import jwt

dotenv.load_dotenv(override=True)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60.0))


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(user_pass: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(user_pass.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
