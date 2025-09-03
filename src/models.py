import datetime

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr



class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=8)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    posts: list["Post"] | None = Relationship(back_populates="user")


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field()
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime | None = Field(default=None)

    user_id: int = Field(foreign_key="user.id")
    user: User|None = Relationship(back_populates="posts")