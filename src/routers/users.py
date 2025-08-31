from fastapi import APIRouter, status, HTTPException
from src import schemas, db, models
from sqlmodel import select


router = APIRouter(prefix = "/users", tags=["users"])


@router.get("/", response_model=list[schemas.UserOut])
async def get_users_list(session: db.SessionDep):
    users = session.exec(select(models.User))
    return users


@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserSignUp, session: db.SessionDep):
    #todo : error handling needed
    check_username_or_email_existence = session.exec(select(models.User).where(
        (user.username == models.User.username) | (models.User.email == user.email))).first()
    if check_username_or_email_existence:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")

    user = models.User(**user.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
