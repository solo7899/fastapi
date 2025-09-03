import datetime
from fastapi import APIRouter, Depends, status, HTTPException, Response
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


@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user: Annotated[models.User, Depends(oauth2.get_current_user)], session: db.SessionDep):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()
    return Response(content="Message deleted successfully", status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{post_id}", response_model=schemas.PostOut)
async def update_post(post_id: int, updated_post: schemas.PostIn, user: Annotated[models.User, Depends(oauth2.get_current_user)], session: db.SessionDep):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.content = updated_post.content
    post.updated_at = datetime.datetime.now(datetime.timezone.utc)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post