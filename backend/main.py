import os

import dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import schemas
from auth.security import create_access_token, verify_password
from crud import links
from database import engine, get_db
from routers import admin, auth

dotenv.load_dotenv(override=True)

is_dev = os.getenv("ENV") == "development"
frontend_app_url = os.getenv("FRONTEND_APP_URL")

templates = Jinja2Templates(directory="templates")

# Crée les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/docs" if is_dev else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin.router)
app.include_router(auth.router)


@app.post("/auth/login")
def login(
    request: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    # Chercher user
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Vérifier password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Token
    token = create_access_token(data={"sub": str(user.id), "role": str(user.role)})

    response = JSONResponse(content={"message": "login success"})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False if is_dev else True,
    )

    return response


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "is_dev": is_dev,
            "doc_url": "/docs" if is_dev else None,
            "redoc_url": "/redoc",
            "frontend_app_url": frontend_app_url if frontend_app_url else None,
        },
    )


@app.post("/links/", response_model=schemas.Link)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    return links.create_link(db=db, link=link)


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_link = links.get_link_by_short_code(db, short_code=short_code)
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=str(db_link.original_url), status_code=301)
