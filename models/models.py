from typing import List
from sqlalchemy import ForeignKey
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    name: Mapped[str]
    role: Mapped[str] = mapped_column(default='user')
    tests: Mapped[List["Test"]] = relationship(back_populates='user', cascade='save-update, merge, delete', passive_deletes=True)
    
class Qa(Base):
    __tablename__ = "qa"
    test_id: Mapped[int] = mapped_column(ForeignKey('test.id', ondelete='CASCADE'), index=True, primary_key=True)
    question: Mapped[str]
    answer: Mapped[str]
        
class Test(Base):
    __tablename__ = "test"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), index=True)
    qa: Mapped[List["Qa"]] = relationship(back_populates='qa', cascade='save-update, merge, delete', passive_deletes=True)
    user: Mapped["User"] = relationship(back_populates='tests')
    

    
