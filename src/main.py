from fastapi import FastAPI
from .routers import users, auth

app = FastAPI()

app.include_router(router=users.router)
app.include_router(router=auth.router)

@app.get("/")
async def root():
    return "Hello world"