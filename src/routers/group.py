from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlmodel import select

from src import oauth2, models, db, schemas


router = APIRouter(prefix="/groups", tags=["group"])

@router.get("/", response_model=list[schemas.GroupOut])
async def get_group_list(session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    groups = session.exec(select(models.Group)).all()
    return groups


@router.get("/{user_id}", response_model=list[schemas.GroupBase])
async def get_user_groups(user_id: int, session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    user_groups = session.exec(select(models.Group).join(models.User.groups).where(models.User.id == user_id)).all()
    return user_groups


@router.post("/create", response_model=schemas.GroupOut, status_code=status.HTTP_201_CREATED)
async def create_group(group: schemas.GroupIn, session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    new_group = models.Group(**group.model_dump())
    session.add(new_group)
    session.commit()
    session.refresh(new_group)
    return new_group
