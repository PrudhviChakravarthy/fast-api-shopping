from .common import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UUID, DECIMAL, DateTime,Text
from uuid import uuid4
from .users import User
from .product import Product
from sqlalchemy.sql import func

class Orders(Base):
    __tablename__ = "orders"
    # __table_args__ = {"schema": "prudvitestschema"}
    order_id = Column(UUID,primary_key=True,  index= True)
    user_id = Column(UUID, ForeignKey(User.user_id), nullable=False)
    product_id = Column(UUID, ForeignKey(Product.product_id), nullable= False)
    quantity = Column(Integer, nullable=False, default= 1)
    price = Column(DECIMAL(precision=15,scale=2), nullable=False)
    total_price = Column(DECIMAL(precision= 15, scale=2), nullable=False)
    ordered_at = Column(DateTime(timezone=True),default= func.now(), nullable=False)
