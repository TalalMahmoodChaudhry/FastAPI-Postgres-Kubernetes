from src.app.schemas.base_schemas import AuthorCreate, BookCreate
from src.app.models.base_models import LanguagesEnum


email = 'test@test.com'
name = 'Test Author'
VALID_AUTHOR_CREATE_PAYLOAD = AuthorCreate(email=email, name=name)

title = 'My First Book'
description = 'This is my first book'
language = LanguagesEnum.urdu
VALID_BOOK_CREATE_PAYLOAD = BookCreate(title=title, language=language, description=description)
VALID_BOOK_CREATE_PAYLOAD.language = language.value

required_params = {
    "detail": [
        {
            "loc": ["body", "username"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "password"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}