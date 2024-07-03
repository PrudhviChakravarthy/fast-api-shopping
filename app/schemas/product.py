from pydantic import BaseModel, constr, condecimal,conint
from pydantic_core import PydanticCustomError
from typing import Optional

class ProductModel(BaseModel):
    name : constr(min_length=10, max_length=100)
    description : constr(min_length= 10, max_length= 250)
    price : condecimal(ge=1.00,max_digits=15,decimal_places=2) 
    quantity : conint(ge = 1)


class UpdateProductModel(BaseModel):
    name : Optional[constr(min_length= 10, max_length= 100)] = None
    price : Optional[condecimal(ge=1.00,max_digits=10,decimal_places=2)] = None
    description : Optional[constr(min_length= 10, max_length= 250)] = None
    quantity : Optional[conint(ge=1)] = None

