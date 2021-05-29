from src.app.schemas import AuthorCreate, BookCreate
from src.libs.constants import LanguagesEnum

email = 'test@test.com'
name = 'Test Author'
VALID_AUTHOR_CREATE_PAYLOAD = AuthorCreate(email=email, name=name)

title = 'My First Book'
description = 'This is my first book'
language = LanguagesEnum.urdu
VALID_BOOK_CREATE_PAYLOAD = BookCreate(title=title, language=language, description=description)
VALID_BOOK_CREATE_PAYLOAD.language = language.value
