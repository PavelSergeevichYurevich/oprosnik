from typing import List, Optional
from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    email: str
    hashed_password: Optional[str] = None
    name: str
        
class UserUpdateSchema(UserCreateSchema):
    password: str
    role: str
    
class QuestionAnswerSchema(BaseModel):
    question: str
    answer: str
    
class TestCreateSchema(BaseModel):
    user_id: int
    



    
