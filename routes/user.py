from typing import List
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from routes.auth import hashing_pass
from dependencies.dependency import get_db
from models.models import User
from schemas.schemas import UserCreateSchema, UserUpdateSchema

user_router = APIRouter(
    prefix='/user',
    tags=['Users']
)
templates = Jinja2Templates(directory="templates")

# вывести пользoвателей
@user_router.get("/show/", response_model=List[UserCreateSchema])
async def get_users(request:Request, db: Session = Depends(get_db)):
    stmnt = select(User)
    users:list = db.scalars(stmnt).all()
    return users

# создать пользователя
@user_router.post("/add/", response_model=UserCreateSchema)
async def add_user(request:Request, user: UserCreateSchema, password: str, db: Session = Depends(get_db)):
    hashed_password = hashing_pass(password)
    new_user = User(
        email = user.email,
        hashed_password = hashed_password,
        name = user.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    # return RedirectResponse(url="/app/login/", status_code=status.HTTP_302_FOUND)

# изменить пользователя
@user_router.put(path='/update/')
async def change_user(request:Request, user_id:int, user_upd: UserUpdateSchema, db: Session = Depends(get_db)):
    hashed_password = hashing_pass(user_upd.password)
    stmnt = update(User).where(User.id == user_id).values(
        email = user_upd.email,
        hashed_password = hashed_password,
        name = user_upd.name,
        role = user_upd.role,
    )
    user = db.execute(stmnt)
    db.commit()
    return user

# удалить пользователя
@user_router.delete(path='/delete/')
async def del_user(request:Request, id:int, db: Session = Depends(get_db)):
    stmnt = delete(User).where(User.id == id)
    user = db.execute(stmnt)
    db.commit()
    return user