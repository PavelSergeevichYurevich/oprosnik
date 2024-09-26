from typing import List
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from dependencies.dependency import get_db
from models.models import User, Test, Qa
from schemas.schemas import TestCreateSchema, QuestionAnswerSchema

start_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@start_router.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

@start_router.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="login.html")

@start_router.get("/register/")
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="register.html")

@start_router.get("/users/{email}")
async def get_tests_page(request:Request, email:str, db: Session = Depends(get_db)):
    stmnt = select(User).where(User.email == email)
    context = db.scalars(stmnt).one()
    return templates.TemplateResponse("users.html", {"request": request, "context": context})