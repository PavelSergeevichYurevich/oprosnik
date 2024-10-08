from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from dependencies.dependency import get_db
from models.models import User

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
    from random import sample
    questions:dict = {
        'Citizenship': {
            'right': 'Russian Federation',
            'wrong': 'Ukraine'
        },
        'Education': {
            'right': 'TOP Academy',
            'wrong': 'ПТУ-39'
        },
        '2*2': {
            'right': '4',
            'wrong': '5'
        },
        '3+2': {
            'right': '5',
            'wrong': '4'
        },
        '3+3': {
            'right': '6',
            'wrong': '5'
        },
        '3*8': {
            'right': '24',
            'wrong': '10'
        },
        '10*8': {
            'right': '80',
            'wrong': '13'
        },
    }
    context:list = [{'email': email}]
    data = list(questions.items())
    choise:tuple = sample(data, 5)
    for item in choise:
        el:dict = {}
        el[item[0]] = item[1]
        context.append(el)
    return templates.TemplateResponse("test.html", {"request": request, "context": context})

@start_router.get("/users/{email}")
async def get_tests_page(request:Request, email:str, db: Session = Depends(get_db)):
    stmnt = select(User).where(User.email == email)
    context = db.scalars(stmnt).one()
    return templates.TemplateResponse("users.html", {"request": request, "context": context})