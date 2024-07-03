from typing import Any
from jwt import DecodeError
from jwt.algorithms import get_default_algorithms
from app.db_connect.database import SessionLocal
from fastapi import status
from fastapi.responses import JSONResponse
from app.db_connect.models.users import User
import jwt
import os

get_default_algorithms()

# db_dependency = Annotated[Session,Depends(get_db)]
JWT_SECRET = os.getenv("JWT_SECRET")

def create_token(paylaod : Any ) -> str:
    token = jwt.encode(payload=paylaod, key=JWT_SECRET, algorithm="HS256")
    return token

def decode_token(token:str):
    try:
        token = token.split(" ")[1]
        userdetails = jwt.decode(token, key=JWT_SECRET,algorithms="HS256")
        return userdetails
    except DecodeError as e:
        return  JSONResponse(status_code=status.HTTP_409_CONFLICT,content= f"decode error please login again")
    except AttributeError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content= f"no token provided")



def get_current_user_id(token : str) -> bool:
    user_details = decode_token(token=token)
    db = SessionLocal()
    user_id = user_details.get('user_id')
    try:
        check_user = db.query(User).filter(User.user_id == user_id).first()
        user_id = check_user.user_id if check_user else None
    except Exception as e:
        print(e)
        return None
    if not user_id:
        return None 
    return user_id

