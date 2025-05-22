from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from fastapi.exceptions import HTTPException
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)
session = Session(bind=engine)

@order_router.get("/")
async def get_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token is invalid")
        
    return {"message": "Order route"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token is invalid")
        
    current_user= Authorize.get_jwt_subject()
    user= session.query(User).filter(User.username==current_user).first()
    new_order= Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size
        
    )
    new_order.user=user
    session.add(new_order)
    session.commit()

    response= {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }
    
 
    return jsonable_encoder(response)

@order_router.get("/orders") #list all orders
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        
    current_user= Authorize.get_jwt_subject()
    user= session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        orders= session.query(Order).all()
        
        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=403, detail="You are not authorized to view all orders or superuser")





@order_router.get("/orders/{id}")  #get order by id
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        
    user= Authorize.get_jwt_subject()
    current_user= session.query(User).filter(User.username==user).first()
    if current_user.is_staff:
        order= session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)
    raise HTTPException(status_code=403, detail="You are not authorized to view this order or superuser")
    



@order_router.get("/user/order")  #get orders by user
async def get_orders_by_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        
    user= Authorize.get_jwt_subject()
    current_user= session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)
    
    
    
@order_router.get("/user/order/{id}/")  #get orders by user
async def get_specific_order(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        
    subject= Authorize.get_jwt_subject()
    current_user= session.query(User).filter(User.username==subject).first()
    orders= current_user.orders

    for o in orders:
        if o.id==id:
            return jsonable_encoder(o)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order not found with such id")
    
    
@order_router.put("/order/update/{id}/")  #update order
async def update_order(id: int, order:OrderModel ,Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    order_to_update = session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity= order.quantity
    order_to_update.pizza_size= order.pizza_size
    session.commit()

    response ={
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "id": order_to_update.id,
        "order_status": order_to_update.order_status
        
   }
    return jsonable_encoder(response)



@order_router.patch("/order/update/{id}/")  #update order status
async def update_order_status(id: int,order:OrderStatusModel ,Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        
    username= Authorize.get_jwt_subject()
    current_user= session.query(User).filter(User.username==username).first()
    if current_user.is_staff:
        order_to_update= session.query(Order).filter(Order.id==id).first()
        order_to_update.order_status= order.order_status
        session.commit()

        response ={
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "id": order_to_update.id,
        "order_status": order_to_update.order_status
        
   }
        return jsonable_encoder(response)
    

@order_router.delete("/order/delete/{id}/", status_code=status.HTTP_204_NO_CONTENT)  #delete order
async def delete_an_order(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        
    order_to_delete= session.query(Order).filter(Order.id==id).first()
    session.delete(order_to_delete)
    session.commit()

    return order_to_delete