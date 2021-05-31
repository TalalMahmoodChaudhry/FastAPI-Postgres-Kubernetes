from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.app import Api
from src.app.schemas import base_schemas
from src.app.services import db_service
from src.app.services.user_authenticate_service import get_current_active_user


@Api().post("/authors", response_model=base_schemas.Author)
def create_author(author: base_schemas.AuthorCreate, db: Session = Depends(db_service.get_db),
                  token: str = Depends(get_current_active_user)):
    db_author = db_service.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this Email already registered")
    return db_service.create_author(db=db, author=author)


@Api().get("/authors", response_model=List[base_schemas.Author])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(db_service.get_db)):
    authors = db_service.get_authors(db, skip=skip, limit=limit)
    return authors


@Api().get("/authors/{author_id}", response_model=base_schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(db_service.get_db)):
    db_author = db_service.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@Api().get("/authors/email/{email}", response_model=base_schemas.Author)
def get_author_by_email(email: str, db: Session = Depends(db_service.get_db)):
    db_author = db_service.get_author_by_email(db, email=email)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
