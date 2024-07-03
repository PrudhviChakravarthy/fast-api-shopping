from fastapi import APIRouter,Depends, Request
from app.schemas.users import SignupModel,LoginModel
from app.services import users
from app.db_connect.database import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/user", tags=['user'])

@router.post("/signup")
def add_user( data : SignupModel , db:Session = Depends(get_db) ):
        return users.create_user_service(data,db)


@router.post("/login",status_code=200)
def login_user(login_data: LoginModel,db:Session = Depends(get_db)):
        token = users.login_service(login_data,db)
        return {"token":token}


    
    

        
        