import pytest

from fastapi.testclient import TestClient

from src import main
from test.test_constants import email, required_params, VALID_AUTHOR_CREATE_PAYLOAD, VALID_BOOK_CREATE_PAYLOAD

client = TestClient(main.Api())


def test_login_bad_data():
    response = client.post("/login_for_access_token", data=None)
    assert response.status_code == 422
    assert response.json() == required_params


def test_login_bad_username():
    response = client.post("/login_for_access_token", data={"username": "bad", "password": "secret"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_bad_password():
    response = client.post("/login_for_access_token", data={"username": "talal", "password": "bad"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login(request):
    response = client.post("/login_for_access_token", data={"username": "talal", "password": "secret"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.status_code == 200
    assert 'access_token' in response.json()

    request.config.cache.set('token', response.json()['access_token'])


@pytest.mark.order(after="test_login")
def test_create_author(request):
    token = request.config.cache.get('token', None)
    response = client.post('/authors', json=VALID_AUTHOR_CREATE_PAYLOAD.dict(), headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json() == {"email": email, "name": "Test Author", "id": 1, "books": []}


@pytest.mark.order(after="test_create_author")
def test_create_author_duplicate_return_error(request):
    token = request.config.cache.get('token', None)
    response = client.post('/authors', json=VALID_AUTHOR_CREATE_PAYLOAD.dict(), headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400
    assert response.json() == {"detail": "Author with this Email already registered"}


@pytest.mark.order(after="test_create_author")
def test_get_author_by_email(request):
    token = request.config.cache.get('token', None)
    response = client.get(f'/authors/email/{email}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json() == {"email": "test@test.com", "name": "Test Author", "id": 1, "books": []}


def test_create_author_no_auth_error():
    response = client.post('/authors', json=VALID_AUTHOR_CREATE_PAYLOAD.dict())
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.order(after="test_get_author_by_email")
def test_create_book_for_author(request):
    token = request.config.cache.get('token', None)
    headers = {'Authorization': f'Bearer {token}'}

    author_object = client.get(f'/authors/email/{email}', headers=headers)
    author_id = author_object.json()['id']
    response = client.post(f'/books/{author_id}', json=VALID_BOOK_CREATE_PAYLOAD.dict(), headers=headers
                           )
    assert response.status_code == 200
    assert response.json() == {'author_id': 1, 'description': 'This is my first book', 'id': 1, 'language': 'Urdu',
                               'title': 'My First Book'}


@pytest.mark.order(after="test_get_author_by_email")
def test_create_book_for_author_no_auth_error(request):
    author_object = client.get(f'authors/email/{email}')
    author_id = author_object.json()['id']
    response = client.post(f'/books/{author_id}', json=VALID_BOOK_CREATE_PAYLOAD.dict())

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.order(after="test_save_book_of_author")
def test_get_author_by_email_with_one_book(request):
    token = request.config.cache.get('token', None)
    headers = {'Authorization': f'Bearer {token}'}

    response = client.get(f'authors/email/{email}', headers=headers)

    assert response.status_code == 200
    assert response.json() == {"email": "test@test.com", "name": "Test Author", "id": 1,
                               "books": [{'author_id': 1, 'description': 'This is my first book', 'id': 1, 'language': 'Urdu',
                                          'title': 'My First Book'}]}
