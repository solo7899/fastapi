from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)

class UserSignUp(UserBase):
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    #todo: add posts list


class PostBase(BaseModel):
    content: str = Field(max_length=100)


class PostIn(PostBase):
    #todo: later it will get it from JWT
    user_id: int


class PostOut(PostBase):
    id: int
    content: str
    created_at: datetime
    user: UserOut