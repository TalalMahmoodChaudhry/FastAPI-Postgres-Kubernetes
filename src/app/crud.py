from sqlalchemy.orm import Session

from src.app import models, schemas


def get_author(db:Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_email(db: Session, email: str) -> schemas.Author:
    return db.query(models.Author).filter(models.Author.email == email).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    author_item = models.Author(name=author.name, email=author.email)
    db.add(author_item)
    db.commit()
    db.refresh(author_item)
    return author_item


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_item = models.Book(**book.dict(), author_id=author_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_books_by_author_email(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()
