from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from auth import create_token, verify_token
import model, schemas
from database import Base, engine, SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "This is the home page of the project"
    }

#login 
@app.post("/login")
def login():
    return{
       "access_token":create_token({"user":"admin"}),
       "token_type":"bearer"

    }



@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), user = Depends(verify_token)):
    new_blog = model.Blog(
        title=blog.title,
        content=blog.content
    )
    try:
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    return new_blog

# read all
@app.get("/blogs", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    return db.query(model.Blog).all()
#read 1 blog 
@app.get("/blogs/{blog_id}",response_model=schemas.BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog =db.query(model.Blog).filter(model.Blog.id== blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")
    return blog 
#update 
@app.put("/update/{blog_id}",response_model=schemas.BlogResponse)
def update_blog(blog_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db), user= Depends(verify_token)):
    existing_blog = db.query(model.Blog).filter(model.Blog.id == blog_id).first()
    
    if not existing_blog:
        raise HTTPException(status_code=404, detail="blog not found")
    
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog

#delete
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == blog_id).first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="blog not found")
    
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

