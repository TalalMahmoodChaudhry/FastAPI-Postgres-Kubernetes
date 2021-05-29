from typing import List, Optional
import json

from pydantic import BaseModel

from src.libs.constants import LanguagesEnum


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
