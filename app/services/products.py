from fastapi import HTTPException
from app.db_connect.models.product import Product
from uuid import UUID
import uuid

def add_product(product_data : dict,current_user_id : UUID, db):
        product = Product(
            product_id = uuid.uuid4(),
            seller_id = current_user_id,
            product_name = product_data.name,
            description = product_data.description,
            price = product_data.price,
            quantity = product_data.quantity)
        db.add(product)
        db.commit()
        return "product added successfully"


def remove_product(product_id : UUID,current_user_id : UUID,  db):
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
                raise HTTPException(status_code= 404, detail="no product available ")
        if str(product.seller_id) != current_user_id:
                raise HTTPException(status_code=403, detail="unauthorized")   
        db.delete(product)
        db.commit()    
        return "product removed"      
                
        
def get_all_products(db):
        output = db.query(Product).all()
        products = {
                str(x.product_id):
                    {"name":x.product_name,
                     "description":x.description,
                     "price":x.price,
                     "quantity":x.quantity} for x in output}
        return products       

def get_single_product(product_id :UUID, db):
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
                raise HTTPException(status_code=404,detail="product with id not found")
        return {product.product_id : {
                "name":product.product_name,
                "description":product.description, 
                "price":product.price, 
                "added":product.added_at,
                "quantity":product.quantity}}

def update_product_service(product_id : UUID,  current_user_id : UUID,product_details : dict, db):
        product_name = product_details.name
        product_price = product_details.price
        product_description = product_details.description
        product_quantity = product_details.quantity

        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
                raise HTTPException(status_code=404,detail="product with id not found")
        print(product.seller_id, current_user_id)
        if product.seller_id  != current_user_id:
                raise HTTPException(status_code=403, detail = "unauthorized")
        
        product.product_name = product_name or product.product_name
        product.price = product_price or product.price
        product.quantity = product_quantity or product.quantity
        product.description = product_description or product.description
        db.commit()
        return "Product updation completed"

        