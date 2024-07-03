from .common import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UUID, Float, DateTime,Text, DECIMAL
from uuid import uuid4
from .users import User
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = "products"
    # __table_args__ = {"schema": "prudvitestschema"}
    product_id = Column(UUID,default=uuid4(),primary_key=True,  index= True)
    product_name = Column(String(100), nullable=False)
    seller_id  =Column(UUID,ForeignKey(User.user_id))
    quantity = Column(Integer, nullable=False, default= 0)
    price = Column(DECIMAL(precision=15,scale=2), nullable=False)
    description = Column(Text,nullable= False)
    added_at = Column(DateTime(timezone=True),default= func.now(), nullable=False)
