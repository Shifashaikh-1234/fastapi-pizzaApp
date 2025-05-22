from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int] 
    username: str
    email: str
    password: str
    is_active: Optional[bool] 
    is_staff: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "shifanx",
                "email": "shifatazeen.msc@gmail.com",
                "password": "password",
                "is_active": True,
                "is_staff": False
            }
        }
        
class Settings(BaseModel):
    authjwt_secret_key: str='60a6c3a47240ecad5f5f3aec715ecc55c4ab334601f0b5a3b040ecc3a6f42d3e'
   
    

   



class LoginModel(BaseModel):
    username: str
    password: str


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "shifanx",
                "password": "password"
            }
        }


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str]= "PENDING"
    pizza_size: Optional[str]= "SMALL"
    user_id: Optional[int]
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE",
               
            }
        }
        

class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }

        
        
    




   
  