from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timedelta
from ..database import cursor
from ..oauth2 import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from ..password import verify_password

router = APIRouter(
    prefix='/authentications',
    tags=['Authentications']
)

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
    else :
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user[7]}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}