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

@start_router.get('/start/{email}')
async def start(request:Request, email: str):
    return templates.TemplateResponse("start.html", {"request": request, "context": email})

@start_router.get('/test/{email}')
async def go_test(request:Request, email:str):
    from random import randint
    questions:dict = {
        1: 'Age',
        2: 'Weight',
        3: 'Height',
        4: 'Male',
        5: 'Education',
        6: 'Hobby',
        7: 'Sport',
        8: 'Car',
        9: 'Army',
        10: 'Work',
    }
    context:dict = {'email': email}
    i:int = 1
    while len(context) < 6:
        key:int = randint(1, 10)
        if questions[key] in context.values():
            continue
        else:
            context[i] = questions[key]
            i = i + 1
    return templates.TemplateResponse("test.html", {"request": request, "context": context})

@start_router.get("/users/{email}")
async def get_tests_page(request:Request, email:str, db: Session = Depends(get_db)):
    stmnt = select(User).where(User.email == email)
    context = db.scalars(stmnt).one()
    return templates.TemplateResponse("users.html", {"request": request, "context": context})