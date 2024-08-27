from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from typing import Annotated
from models import get_db
from schemas import PostBase
from services import post_services
from .limiter import limiter

router = APIRouter(prefix="/posts")

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/second")
async def create_post(request:Request, post: PostBase, db: db_dependency):
    db_post = post_services.create_post(db, post)
    return db_post

@router.get("/{post_id}", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
async def read_post(request:Request, post_id: int, db: db_dependency):
    post = post_services.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
async def delete_post(request:Request, post_id: int, db: db_dependency):
    db_post = post_services.delete_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"detail": "Post deleted successfully"}
