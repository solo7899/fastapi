from fastapi import APIRouter
from src import schemas, db, models
from sqlmodel import select


router = APIRouter(prefix = "/users", tags=["users"])

users = [
    {
        'id': 1,
        'username': 'hrd',
        'email': 'hrd@gmail.com',
        'password': 'password',
        'created_at': '2025-06-15 14:30:00'
    },
    {
        'id': 2,
        'username': 'hrd_d',
        'email': 'hrd_d@gmail.com',
        'password': 'password',
        'created_at': '2024-03-01 11:30:00'
    }
]
@router.get("/", response_model=list[schemas.UserOut])
async def get_users_list(session: db.SessionDep):
    users = session.exec(select(models.User))
    return users