from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from dependencies.dependency import get_db
from models.models import User, Test, Qa

test_router = APIRouter(
    prefix='/test',
    tags=['Tests']
)
templates = Jinja2Templates(directory="templates")

@test_router.get("/show/")
async def get_tests(request:Request, user_id:int, db: Session = Depends(get_db)):
    stmnt = select(Test).where(Test.user_id == user_id)
    tests:list = db.scalars(stmnt).all()
    return tests

# создать test
@test_router.post("/add/")
async def add_test(request:Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)
    print(da)
    email:str = da['email']
    stmnt = select(User).where(User.email == email)
    user_id = db.scalars(stmnt).one().id
    del da['email']
    new_test = Test(
        user_id = user_id, 
        )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    for k, v in da.items():
        new_questansw = Qa(
            test_id = new_test.id,
            question = k,
            answer = v
        )
        db.add(new_questansw)
        db.commit()
        db.refresh(new_questansw)
    return new_test

# удалить test
@test_router.delete(path='/delete/')
async def del_test(request:Request, test_id:int, db: Session = Depends(get_db)):
    stmnt = delete(Test).where(Test.id == test_id)
    test = db.execute(stmnt)
    db.commit()
    return test



    
