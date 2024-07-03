from pydantic import BaseModel, conint,condecimal
from typing import Optional

class OrderModel(BaseModel):
    quantity : conint(ge=1)
    price : Optional[condecimal(ge=1.00,max_digits=15,decimal_places=2) ] = None

