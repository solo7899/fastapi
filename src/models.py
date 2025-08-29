from sqlmodel import SQLModel, Field
from pydantic import EmailStr



class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True, unique=True)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False, min_length=8)