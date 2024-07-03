import uvicorn
from fastapi import FastAPI,Request,BackgroundTasks,Depends
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.controllers.authorize import  get_current_user_id
from app.routes import (
    users,
    products,
    orders,
    tracking
)
from sqlalchemy.orm import Session
from app.db_connect.database import get_db
from app.db_connect.models.users import User
from typing import Annotated
import logging
import time

app = FastAPI()
logging_tasks = BackgroundTasks()



logging.basicConfig(
    level=logging.DEBUG ,
    filename="logging.txt", 
    filemode="a",
    datefmt='%Y-%m-%d %H:%M:%S', 
    format='%(asctime)s - %(message)s'
    )

logging = logging.getLogger(__name__)

app.add_middleware(CORSMiddleware, 
                   allow_origins = ["http://localhost:8081"],
                   allow_headers = ["*"],
    
                   )

def add_logging_data(url:str, method: str, body: dict)-> None:
        logging.info(f'{url} - {method} ->  {body}')
        time.sleep(2)
        print(url)


@app.middleware("http")
async def add_user_id_with_token(request:Request, call_next):
    calls = ['user/login','user/signup']
    skip_calls = [str(request.base_url) + x for x in calls]
    ## checks for which calls to skip
    if request.url in skip_calls:
        return await call_next(request)
    # checks for headers for token
    token = request.headers.get("Authorization") or None
    if not token:
        return JSONResponse(status_code= 404, content= "No token provided")
    #decodes token
    user = get_current_user_id(token)
    if not user:
        return JSONResponse(status_code= 404, content= "No user found")    
    request.state.user_id = user
    return await call_next(request)

    
@app.middleware('http')
async def logging_middleware(request: Request, call_next):
    url = request.url
    method = request.method
    req_body = await request.body()
    logging.info(f'{url} - {method} ->  {req_body.decode() or ""}')
    # logging_tasks.add_task(func=add_logging_data,url= url, method = method, body = req_body)
    return await call_next(request)



# app.include_router(comments.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(tracking.router)

if "__main__" == __name__:
    uvicorn.run(app,port=8090,reload=True)