from typing import List, Optional

from pydantic import BaseModel

from src.app.models.base_models import LanguagesEnum


class BookCreate(BaseModel):
    title: str
    language: LanguagesEnum
    description: Optional[str]


class Book(BookCreate):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    email: str
    name: str


class Author(AuthorCreate):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
