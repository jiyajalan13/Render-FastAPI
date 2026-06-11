# Render FastAPI

A simple FastAPI blog API project.

## Features

- Create blog posts
- Read all blog posts
- Read a single blog post
- Update blog posts
- Delete blog posts
- JWT token authentication for protected routes

## Files

- `main.py` - FastAPI application and route definitions
- `database.py` - SQLAlchemy database configuration
- `model.py` - Blog model definition
- `schemas.py` - Pydantic request/response schemas
- `auth.py` - JWT token creation and verification
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python -m uvicorn main:app --reload
   ```

## API Endpoints

- `GET /` - Home endpoint
- `POST /login` - Get an access token
- `POST /blogs` - Create a blog post
- `GET /blogs` - Read all blog posts
- `GET /blogs/{blog_id}` - Read one blog post
- `PUT /update/{blog_id}` - Update a blog post
- `DELETE /blogs/{blog_id}` - Delete a blog post

## Notes

- The app currently uses SQLite by default (`blog.db`).
- Use a `.env` file to override `DATABASE_URL` if needed.
