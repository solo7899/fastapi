from fastapi import APIRouter, status, HTTPException, Depends
from src import schemas, db, models, oauth2
from sqlmodel import select
from typing import Annotated

from . import auth

#todo: make everything token dependant
router = APIRouter(prefix = "/users", tags=["users"])


@router.get("/", response_model=list[schemas.UserOut])
async def get_users_list(session:  db.SessionDep, current_user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    users = session.exec(select(models.User))
    return users


@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserSignUp, session: db.SessionDep):
    check_username_or_email_existence = session.exec(select(models.User).where(
        (user.username == models.User.username) | (models.User.email == user.email))).first()
    if check_username_or_email_existence:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")

    user.password = auth.get_password_hash(user.password)
    user = models.User(**user.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# @router.post("/signin", response_model=schemas.UserOut)
# @router.post('/signin', response_model=schemas.Token)
# async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     return auth.login_for_access_token(form_data=form_data)
