from pydantic import BaseModel, EmailStr, constr, model_validator, ValidationInfo
from pydantic_core import PydanticCustomError

class SignupModel(BaseModel):
    email : EmailStr
    first_name : constr(min_length=2,max_length=60)
    last_name : constr(min_length=4,max_length=60)
    password : constr(min_length= 8 , max_length= 64 , pattern=r'^[A-Za-z1-9]+$')
    confirm_password : constr(min_length= 8 , max_length= 64 , pattern=r'^[A-Za-z1-9]+$')

    @model_validator(mode = "wrap")
    def validate_passowords_match(cls, values, info : ValidationInfo):
        if values.get("password") != values.get("confirm_password"):
            raise PydanticCustomError("password match error", f"password and confirm password are not match ")
        else:
            return values
        
class LoginModel(BaseModel): 
    email : EmailStr
    password : constr(min_length= 8 , max_length= 64 , pattern=r'^[A-Za-z1-9]+$')