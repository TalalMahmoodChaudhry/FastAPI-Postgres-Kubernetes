import enum

from sqlalchemy import ForeignKey, Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from src.app.database import Base


class LanguagesEnum(str, enum.Enum):
    english = "English"
    french = "French"
    german = "German"
    chinese = "Chinese"
    arabic = "Arabic"
    urdu = "Urdu"


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)

    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    language = Column(Enum(LanguagesEnum), index=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    description = Column(String, index=True)

    owner = relationship("Author", back_populates="books")
