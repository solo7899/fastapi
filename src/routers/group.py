from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlmodel import select

from src import oauth2, models, db, schemas


router = APIRouter(prefix="/groups", tags=["group"])

@router.get("/", response_model=list[schemas.GroupOut])
async def get_group_list(session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    groups = session.exec(select(models.Group)).all()
    return groups


@router.get("/{usr_name}", response_model=list[schemas.GroupBase])
async def get_user_groups(usr_name: str, session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    user_groups = session.exec(select(models.Group).join(models.User.groups).where(models.User.username == usr_name)).all()
    return user_groups


@router.post("/create", response_model=schemas.GroupOut, status_code=status.HTTP_201_CREATED)
async def create_group(group: schemas.GroupIn, session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    new_group = models.Group(**group.model_dump())
    session.add(new_group)
    session.commit()
    session.refresh(new_group)
    return new_group

@router.post("/{group_name}/join", response_model=schemas.GroupOut)
async def join_group(group_name: str, session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    group = session.exec(select(models.Group).where(models.Group.name == group_name)).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if user in group.members:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already a member of this group")
    group.members.append(user)
    session.add(group)
    session.commit()
    session.refresh(group)
    return group
