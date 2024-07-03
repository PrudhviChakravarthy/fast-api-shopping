from fastapi import APIRouter, Request
from fastapi import Depends
from uuid import UUID
from app.services import orders
from app.schemas.orders import OrderModel
from app.db_connect.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/order", tags=['order'])

@router.post("/{product_id}")
def create_order_route(product_id: UUID,request : Request, order_data : OrderModel , db:Session = Depends(get_db)):
        quantity = order_data.quantity
        current_user = request.state.user_id
        return orders.create_order_service(product_id = product_id, current_user_id=current_user,quantity = quantity,db=db)

@router.get("/all")
def get_orders_details_by_id(request:Request, db:Session = Depends(get_db)):
        current_user = request.state.user_id
        return orders.get_orders_by_user_id(current_user_id= current_user,db=db)

@router.get("/{order_id}")
def get_order_details(order_id : UUID, request : Request, db:Session = Depends(get_db)):
        current_user = request.state.user_id
        return orders.get_order_by_id(order_id = order_id , current_user_id = current_user, db = db)