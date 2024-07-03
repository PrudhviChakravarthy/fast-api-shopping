from fastapi import HTTPException
from app.db_connect.models.users import User
from app.controllers.authorize import create_token
from app.controllers.auth import hash_password, check_password
from sqlalchemy import or_
import time

def create_user_service(user_data : dict,db):
    check_user = db.query(User).filter(User.email == user_data.get("email")).first()
    if not check_user:
        try:
            user = User(
                email = user_data.get("email"),
                first_name = user_data.get("firstname"),
                last_name = user_data.get("lastname"),
                password = hash_password(user_data.get("password")),) 
            db.add(user)
            db.commit()
        except Exception as e:
            print(e)
            return HTTPException(status_code=500)
        return "user created successfully"
    raise HTTPException(status_code=409, detail="user already exists")

def login_service(login_details:dict,db):
    find_user = db.query(User).filter(User.email == login_details.email).first()
    print(find_user.user_id)
    if not  find_user:
        raise HTTPException(status_code= 404, detail='user not found')
    
    passcheck = check_password(login_details.password.encode(),find_user.password.encode())
    if not passcheck:
        raise HTTPException(status_code= 403, detail='password is incorrect')
    
    find_user.last_active = int(time.time())
    token = create_token({"user_id":str(find_user.user_id)})
    db.add(find_user)
    db.commit()
    return token

