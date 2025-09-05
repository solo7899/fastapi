from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import select

from src import oauth2, models, db, schemas


router = APIRouter(prefix="/group", tags=["group"])

@router.get("/", response_model=list[schemas.GroupOut])
async def get_group_list(session: db.SessionDep, user: Annotated[models.User, Depends(oauth2.get_current_user)]):
    groups = session.exec(select(models.Group)).all()
    return groups

