import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src import  schemas, db, oauth2
from src.utils import ACCESS_TOKEN_EXPIRE_HOURS



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: db.SessionDep) -> schemas.Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = oauth2.authenticate_user(form_data.username, form_data.password, session=session)
    if not user:
        raise credentials_exception
    
    access_token_expires = datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = oauth2.create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)

    return schemas.Token(access_token=access_token, token_type='bearer')