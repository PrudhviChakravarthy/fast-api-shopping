from fastapi import APIRouter,Depends, Request
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.product import ProductModel,UpdateProductModel
from app.services import products
from app.db_connect.database import get_db


router = APIRouter(prefix="/product", tags=['product'])

@router.post("")
def add_product_route(request : Request, product_data : ProductModel , db: Session = Depends(get_db)):
        current_user = request.state.user_id
        return products.add_product(product_data= product_data, current_user_id=current_user,db=db)

@router.get("/all")
def get_every_product(db:Session = Depends(get_db)):
        return products.get_all_products(db = db)

@router.get("/{product_id}")
def get_product_details(product_id : UUID, db:Session = Depends(get_db)):
        return products.get_single_product(product_id = product_id , db = db)
        

@router.delete("/{product_id}")
def remove_product_route(product_id :UUID,request: Request,db:Session = Depends(get_db)):
        current_user = request.state.user_id
        return products.remove_product(product_id=product_id, current_user_id= current_user, db = db)

        
@router.put("/{product_id}")
def update_product_route(product_id : UUID, update_product : UpdateProductModel, request : Request, db: Session = Depends(get_db)):
        current_user = request.state.user_id
        return products.update_product_service(product_id=product_id,product_details = update_product,current_user_id = current_user, db =db )
        

