from fastapi import HTTPException
from app.db_connect.models.product import Product
from app.db_connect.models.orders import Orders
from app.db_connect.models.tracking import Tracking
from sqlalchemy import select
from uuid import UUID
import uuid

def check_and_update_product_details(product_id : UUID,quantity : int , db):
        product = db.query(Product).filter(Product.product_id == product_id ).first()
        if not product:
                raise HTTPException(status_code= 404, detail= "product not found ")
        if product.quantity < 1:
                raise HTTPException(status_code=404,detail="Product out of stock" )
        if product.quantity < quantity:
                raise HTTPException(status_code=405, detail= "No much stock in place")
        product.quantity = product.quantity-quantity
        db.commit()
        return product


def create_order_service(product_id:UUID,current_user_id : UUID,quantity : int ,  db):
        product_details =  check_and_update_product_details(product_id= product_id, quantity= quantity, db = db)
        total_price = product_details.price * quantity
        order_id = uuid.uuid4()
        create_order = Orders(
                order_id = order_id,
                product_id = product_id, 
                total_price = total_price, 
                quantity = quantity, 
                price = product_details.price,
                user_id = current_user_id,
                )
        db.add(create_order)
        db.commit()
        return "Order cerated Successfully"

def get_orders_by_user_id( current_user_id : UUID, db):
        orders  = db.query(Orders).filter(Orders.user_id == current_user_id).all()
        if not orders:
                raise HTTPException(status_code=404, detail="orders not found")
        orders = {
                order.order_id:{"total_price":order.total_price,
                            "product_id":order.product_id,
                            "quantity":order.quantity,
                            "product_price":order.price,
                            "ordered_at":str(order.ordered_at)} for order in orders}
        return orders

def get_order_by_id( order_id: UUID, current_user_id : UUID, db):
        order  = db.query(Orders).filter(Orders.order_id == order_id).first()
        if not order:
                raise HTTPException(status_code=404, detail="orders not found")
        if order.user_id != current_user_id:
                raise HTTPException(status_code=403, detail="unauthorized")
        traking = db.query(Tracking).filter(Tracking.order_id == order_id).first()
        traking_id = traking.tracking_id if traking else 0
        return  {"total_price":order.total_price,
                "product_id":order.product_id,
                "quantity":order.quantity,
                "ordered_at":str(order.ordered_at),
                "Tracking_id":traking_id}
