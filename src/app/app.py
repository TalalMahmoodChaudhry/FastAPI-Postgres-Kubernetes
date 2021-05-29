from typing import Dict, List
import logging
import os
import secrets

import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES
from opencensus.trace.span import SpanKind

from src.app import crud, models, schemas
from src.app.database import SessionLocal, engine
from src.libs.constants import user, password
from src.libs.logging_handlers import initialize_logging, get_tracer

HTTP_URL = COMMON_ATTRIBUTES['HTTP_URL']
HTTP_STATUS_CODE = COMMON_ATTRIBUTES['HTTP_STATUS_CODE']

initialize_logging()
logger = logging.getLogger(os.path.basename(__file__))

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_user_password(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, user)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.middleware("http")
async def middleware_opencensus(request: Request, call_next):
    tracer = get_tracer()
    if tracer:
        with tracer.span("main") as span:
            span.span_kind = SpanKind.SERVER

            response = await call_next(request)

            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_STATUS_CODE,
                attribute_value=response.status_code)
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_URL,
                attribute_value=str(request.url))

        return response
    else:
        return await call_next(request)


@app.get('/')
async def read_root() -> Dict:
    return {'API': 'Running'}


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db),
                  credentials: HTTPBasicCredentials = Depends(verify_user_password)):
    db_author = crud.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this Email already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/author_id/{author_id}", response_model=schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/authors/email/{email}", response_model=schemas.Author)
def get_author_by_email(email: str, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_email(db, email=email)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db),
                           credentials: HTTPBasicCredentials = Depends(verify_user_password)):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/authors/{email}", response_model=List[schemas.Book])
def get_books_for_author_by_email(email: str, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_email(db, email=email)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_books_by_author_email(db, db_author.id)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_books(db, skip=skip, limit=limit)
    return items


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=None)
