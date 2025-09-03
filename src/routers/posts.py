from fastapi import APIRouter, Depends
from typing import Annotated

from src import oauth2

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
async def get_posts_list(user: Annotated[str, Depends(oauth2.get_current_user)]):
    return "List of posts"