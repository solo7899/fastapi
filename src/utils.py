import datetime
import jwt
import os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError


load_dotenv()

SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict, expires_delta: datetime.timedelta  | None = None):
    to_encode = data.copy()

    if expires_delta: 
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

    return encoded_jwt