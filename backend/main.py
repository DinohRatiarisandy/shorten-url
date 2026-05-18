from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

# Crée les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/links/", response_model=schemas.Link)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    return crud.create_link(db=db, link=link)


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_link = crud.get_link_by_short_code(db, short_code=short_code)
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=str(db_link.original_url), status_code=301)
