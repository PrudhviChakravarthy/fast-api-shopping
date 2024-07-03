from .common import Base
from sqlalchemy import Column, Integer, String, UUID, DateTime
from sqlalchemy.sql import func
from uuid import uuid4



class User(Base):
    __tablename__ = "users"
    # __table_args__ = {"schema": "prudvitestschema"}
    user_id  =Column(UUID,default= uuid4(), primary_key=True,index=True)
    email = Column(String, nullable= False, unique= True)
    first_name = Column(String, nullable= False)
    last_name = Column(String , nullable=False)
    created_date = Column(DateTime(timezone=True),default=func.now(), nullable=False)
    last_active_date = Column(DateTime(timezone=True),nullable=True)
    password = Column(String, nullable=True)
