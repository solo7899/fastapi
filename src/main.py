from fastapi import FastAPI
from .routers import users, auth, posts

app = FastAPI()

app.include_router(router=users.router)
app.include_router(router=auth.router)
app.include_router(router=posts.router)

@app.get("/")
async def root():
    return "Hello world"