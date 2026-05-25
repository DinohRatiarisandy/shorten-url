import os

import dotenv

import models
from auth.security import hash_password
from database import SessionLocal

dotenv.load_dotenv(override=True)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")

db = SessionLocal()


def is_user_exists(
    email: str, role: models.UserRole = models.UserRole.user
) -> models.User | None:
    """Retourne l'user qui a le email avec le role"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and user.role == role:
        return user


def create_admin():
    hashed_password = hash_password(ADMIN_PASSWORD)
    if not is_user_exists(ADMIN_EMAIL, models.UserRole.admin):
        print("Création du compte admin...")
        db_admin = models.User(
            email=ADMIN_EMAIL,
            hashed_password=hashed_password,
            role=models.UserRole.admin,
        )

        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        print("Compte admin crée avec succès.")
    else:
        print("Compte admin déjà crée.")


if __name__ == "__main__":
    create_admin()
