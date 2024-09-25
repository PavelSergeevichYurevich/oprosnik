from typing import List
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from dependencies.dependency import get_db
from models.models import User, Test, Qa
from schemas.schemas import TestCreateSchema, QuestionAnswerSchema

test_router = APIRouter(
    prefix='/test',
    tags=['Tests']
)
templates = Jinja2Templates(directory="templates")

@test_router.get("/show/")
async def get_tests(request:Request, user_id:int, db: Session = Depends(get_db)):
    stmnt = select(Test).where(Test.user_id == user_id)
    tests:list = db.scalars(stmnt).all()
    for test in tests:
        print(test.questionsanswers)
    return tests

# создать test
@test_router.post("/add/")
async def add_test(request:Request, test: TestCreateSchema, questansw: List[QuestionAnswerSchema], db: Session = Depends(get_db)):
    new_test = Test(
        user_id = test.user_id, 
        )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    for item in questansw:
        new_questansw = Qa(
            test_id = new_test.id,
            question = item.question,
            answer = item.answer
        )
        db.add(new_questansw)
        db.commit()
        db.refresh(new_questansw)
    # return RedirectResponse(url="/app/login/", status_code=status.HTTP_302_FOUND)
    return new_test

# удалить test
@test_router.delete(path='/delete/')
async def del_test(request:Request, test_id:int, db: Session = Depends(get_db)):
    stmnt = delete(Test).where(Test.id == test_id)
    test = db.execute(stmnt)
    db.commit()
    return test



    
