import pytest

from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from src.app.app import app
from src.libs.constants import user, password
from test.test_constants import email, VALID_AUTHOR_CREATE_PAYLOAD, VALID_BOOK_CREATE_PAYLOAD

HEADERS = {'Content-Type': 'application/json'}

client = TestClient(app)


@pytest.mark.order(1)
def test_app_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'API': 'Running'}


@pytest.mark.order(2)
def test_create_author():
    response = client.post('authors/', json=VALID_AUTHOR_CREATE_PAYLOAD.dict(), headers=HEADERS,
                           auth=HTTPBasicAuth(user, password))
    assert response.status_code == 200
    assert response.json() == {"email": "test@test.com", "name": "Test Author", "id": 1, "books": []}


@pytest.mark.order(after="test_create_author")
def test_create_author_duplicate_return_error():
    response = client.post('authors/', json=VALID_AUTHOR_CREATE_PAYLOAD.dict(), headers=HEADERS,
                           auth=HTTPBasicAuth(user, password))
    assert response.status_code == 400
    assert response.json() == {"detail": "Author with this Email already registered"}


@pytest.mark.order(after="test_create_author")
def test_get_author_by_email():
    response = client.get(f'authors/email/{email}', headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"email": "test@test.com", "name": "Test Author", "id": 1, "books": []}


def test_create_author_no_auth_error():
    response = client.post('authors/', json=VALID_AUTHOR_CREATE_PAYLOAD.dict(), headers=HEADERS)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_author_bad_user_pass_error():
    response = client.post('authors/', json=VALID_AUTHOR_CREATE_PAYLOAD.dict(), headers=HEADERS,
                           auth=HTTPBasicAuth('bad-user', 'bad-password'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect email or password'}


@pytest.mark.order(after="test_get_author_by_email")
def test_create_book_for_author():
    author_object = client.get(f'authors/email/{email}', headers=HEADERS)
    author_id = author_object.json()['id']

    response = client.post(f'/books/{author_id}/books/', json=VALID_BOOK_CREATE_PAYLOAD.dict(), headers=HEADERS,
                           auth=HTTPBasicAuth(user, password))
    assert response.status_code == 200
    assert response.json() == {'author_id': 1, 'description': 'This is my first book', 'id': 1, 'language': 'Urdu',
                               'title': 'My First Book'}


@pytest.mark.order(after="test_get_author_by_email")
def test_create_book_for_author_no_auth_error():
    author_object = client.get(f'authors/email/{email}', headers=HEADERS)
    author_id = author_object.json()['id']

    response = client.post(f'/books/{author_id}/books/', json=VALID_BOOK_CREATE_PAYLOAD.dict(), headers=HEADERS)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.order(after="test_get_author_by_email")
def test_create_book_for_author_bad_user_pass_error():
    author_object = client.get(f'authors/email/{email}', headers=HEADERS)
    author_id = author_object.json()['id']

    response = client.post(f'/books/{author_id}/books/', json=VALID_BOOK_CREATE_PAYLOAD.dict(), headers=HEADERS,
                           auth=HTTPBasicAuth('bad-user', 'bad-password'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect email or password'}


@pytest.mark.order(after="test_save_book_of_author")
def test_get_author_by_email_with_one_book():
    response = client.get(f'authors/email/{email}', headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"email": "test@test.com", "name": "Test Author", "id": 1,
                               "books": [{'author_id': 1, 'description': 'This is my first book', 'id': 1, 'language': 'Urdu',
                                          'title': 'My First Book'}]}
