from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey
from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    name: Mapped[str]
    data_create: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    data_change: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    role: Mapped[str] = mapped_column(default='user')
    order: Mapped[List["Order"]] = relationship(back_populates='customer', cascade='save-update, merge, delete', passive_deletes=True)
