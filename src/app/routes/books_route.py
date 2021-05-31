from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.app import Api
from src.app.schemas import base_schemas
from src.app.services.user_authenticate_service import get_current_active_user
from src.app.services import db_service

api = Api()


@api.post("/books/{author_id}", response_model=base_schemas.Book)
def create_book_for_author(author_id: int, book: base_schemas.BookCreate, db: Session = Depends(db_service.get_db),
                           token: str = Depends(get_current_active_user)):
    return db_service.create_book(db=db, book=book, author_id=author_id)


@api.get("/books/{author_email}", response_model=List[base_schemas.Book])
def get_books_for_author_by_email(author_email: str, db: Session = Depends(db_service.get_db)):
    db_author = db_service.get_author_by_email(db, email=author_email)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_service.get_books_by_author_email(db, db_author.id)


@api.get("/books", response_model=List[base_schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(db_service.get_db)):
    items = db_service.get_books(db, skip=skip, limit=limit)
    return items
