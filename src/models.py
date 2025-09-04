import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr



class User_Group(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=8)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    posts: list["Post"] | None = Relationship(back_populates="user")
    groups: list["Group"] | None = Relationship(back_populates="members", link_model=User_Group)


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field()
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime | None = Field(default=None)

    user_id: int = Field(foreign_key="user.id")
    user: User|None = Relationship(back_populates="posts")

    group_id: int = Field(foreign_key="group.id", default=None)
    group: Optional["Group"]= Relationship(back_populates="posts")


class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    members: list["User"] | None = Relationship(back_populates="groups", link_model=User_Group)
    posts: list["Post"] | None = Relationship(back_populates="group")

