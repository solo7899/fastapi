import datetime
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import select

from src import  schemas, db, models
from src.utils import SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/auth", tags=["auth"])

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, session: db.Session):
    user = get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: datetime.timedelta  | None = None):
    to_encode = data.copy()

    if expires_delta: 
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

    return encoded_jwt

def get_user(username, session: db.Session):
    user = session.exec(select(models.User).where(models.User.username == username )).first()
    if user:
        return user


async def get_current_user(token: Annotated[str , Depends(oauth2_scheme)], session: db.SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokneData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: db.SessionDep) -> schemas.Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = authenticate_user(form_data.username, form_data.password, session=session)
    if not user:
        raise credentials_exception
    
    access_token_expires = datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)

    return schemas.Token(access_token=access_token, token_type='bearer')