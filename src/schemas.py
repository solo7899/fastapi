from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
