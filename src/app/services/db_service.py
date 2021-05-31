from sqlalchemy.orm import Session

from src.app.models import base_models
from src.app.schemas import base_schemas
from src.app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_author(db: Session, author_id: int):
    return db.query(base_models.Author).filter(base_models.Author.id == author_id).first()


def get_author_by_email(db: Session, email: str) -> base_schemas.Author:
    return db.query(base_models.Author).filter(base_models.Author.email == email).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(base_models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: base_schemas.AuthorCreate):
    author_item = base_models.Author(name=author.name, email=author.email)
    db.add(author_item)
    db.commit()
    db.refresh(author_item)
    return author_item


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(base_models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: base_schemas.BookCreate, author_id: int):
    db_item = base_models.Book(**book.dict(), author_id=author_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_books_by_author_email(db: Session, author_id: int):
    return db.query(base_models.Book).filter(base_models.Book.author_id == author_id).all()
