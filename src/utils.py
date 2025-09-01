import jwt
from jwt.exceptions import InvalidTokenError


SECRET = "52d1ec82039927999dddd0537f03ffbd4c582c36a8a94d7f1740c52ce0f275cc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 4