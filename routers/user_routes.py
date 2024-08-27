from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from typing import Annotated
from models import get_db
from schemas import UserBase
from services import user_services
from .limiter import limiter


router = APIRouter(prefix="/users")



db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/second")
async def create_user(request:Request, user: UserBase, db: db_dependency):
    db_user = user_services.create_user(db, user)
    return db_user

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
async def read_user(request:Request, user_id: int, db: db_dependency):
    user = user_services.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
