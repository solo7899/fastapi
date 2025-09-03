# FastAPI Blog API

This is an ongoing project: a RESTful API for a simple blog platform built with FastAPI and SQLModel.

## Features

- User registration and authentication (JWT-based)
- Secure password hashing
- CRUD operations for posts
- Alembic migrations for database schema
- SQLite database (default)
- Modular routers for users, posts, and authentication

## Project Structure

```
alembic.ini
alembic/
    env.py
    README
    script.py.mako
    versions/

src/
    __init__.py
    db.py
    main.py
    models.py
    oauth2.py
    schemas.py
    utils.py
    routers/
        __init__.py
        auth.py
        posts.py
        users.py
requirements.txt
```

## Requirements

All dependencies are listed in `requirements.txt`. Key packages include:

- fastapi
- sqlmodel
- alembic
- uvicorn
- passlib
- bcrypt
- pydantic
- python-dotenv
- email-validator

See the full list in `requirements.txt` for exact versions.

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd fastapi
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

- `/users/` - List users (protected)
- `/users/signup` - Register new user
- `/auth/token` - Obtain JWT token
- `/posts/` - CRUD for posts

## Tech Stack

- FastAPI
- SQLModel
- Alembic
- SQLite

## Status

This project is **ongoing** and under active development. Contributions and feedback are welcome!
