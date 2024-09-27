from typing import Optional
from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    email: str
    password: str
    hashed_password: Optional[str] = None
    
class UserShowSchema(BaseModel):
    email: str
        
class UserUpdateSchema(UserCreateSchema):
    role: str
    
class QuestionAnswerSchema(BaseModel):
    question: str
    answer: str
    
class TestCreateSchema(BaseModel):
    user_id: int
    



    
