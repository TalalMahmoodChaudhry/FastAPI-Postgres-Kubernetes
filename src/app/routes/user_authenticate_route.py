from datetime import timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.app import Api
from src.app.schemas.user_authenticate_schemas import Token, User
from src.app.services.user_authenticate_service import authenticate_user, create_access_token, get_current_user
from src.libs.constants import ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db

api = Api()


@api.post("/login_for_access_token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@api.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
