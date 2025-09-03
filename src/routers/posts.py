from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import Annotated

from src import oauth2, db, models, schemas

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[schemas.PostOut])
async def get_posts_list(user: Annotated[str, Depends(oauth2.get_current_user)], session: db.SessionDep):
    posts = session.exec(select(models.Post)).all()
    return posts

