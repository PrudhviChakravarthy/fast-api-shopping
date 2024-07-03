from .common import Base
from sqlalchemy import Column, String, ForeignKey, UUID, DateTime
from uuid import uuid4
from .orders import Orders
from sqlalchemy.sql import func

class Tracking(Base):
    __tablename__ = "tracking"
    # __table_args__ = {"schema": "prudvitestschema"}
    tracking_id = Column(UUID,primary_key=True,  index= True)
    order_id = Column(UUID, ForeignKey(Orders.order_id), nullable=False)
    status = Column(String(20), nullable= False)
    odered_date = Column(DateTime(),default= func.now(), nullable=False)
    shipment_date = Column(DateTime(),nullable=False)
    delevery_date = Column(DateTime(),nullable = False)

