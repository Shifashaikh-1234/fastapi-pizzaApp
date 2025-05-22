from fastapi import APIRouter,status, Depends
from fastapi.exceptions import HTTPException
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session= Session(bind=engine)

#JWT config
@auth_router.get("/")
async def get_auth(Authorize: AuthJWT= Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": "Hello world from auth route"}



#signup route
@auth_router.post("/signup",status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email= session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_username= session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    new_user= User(
        username=user.username,
        email=user.email,
        password= generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
        
    )

    session.add(new_user)
    session.commit()
    
    return new_user


#login route
@auth_router.post("/login",status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT= Depends()):
    db_user= session.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token= Authorize.create_access_token(subject=user.username)
    refresh_token= Authorize.create_refresh_token(subject=user.username)

    
    response= {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    
    return jsonable_encoder(response)
    

#refresh token route
@auth_router.get("/refresh")
async def refresh_token(Authorize: AuthJWT= Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    current_user= Authorize.get_jwt_subject()
    access_token= Authorize.create_access_token(subject=current_user)
    
    response= {
        "access_token": access_token
    }
    
    return jsonable_encoder(response)