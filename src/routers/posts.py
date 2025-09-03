from fastapi import APIRouter, Depends, status
from sqlmodel import select
from typing import Annotated

from src import oauth2, db, models, schemas

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[schemas.PostOut])
async def get_posts_list(user: Annotated[str, Depends(oauth2.get_current_user)], session: db.SessionDep):
    posts = session.exec(select(models.Post)).all()
    return posts


@router.post("/create", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostIn, user: Annotated[models.User, Depends(oauth2.get_current_user)], session: db.SessionDep):
    new_post = models.Post(user_id=user.id, **post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post