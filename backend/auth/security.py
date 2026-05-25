import bcrypt


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(user_pass: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(user_pass.encode("utf-8"), hashed_password.encode("utf-8"))
