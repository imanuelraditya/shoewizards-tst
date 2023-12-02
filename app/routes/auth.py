from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime
from ..database import cursor, conn
from ..oauth2 import create_access_token, authenticate_user
import requests

smartcarttoken = ""

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
        url = "http://localhost:3000/auth/token"
        data = {
                'grant_type': '',
                'username': form_data.username,
                'password': form_data.password,
                'scope': '',
                'client_id': '',
                'client_secret': ''
        }

        response = requests.post(url, data=data)
        print(response.status_code)
        if response.status_code == 200 :
            try :
                print(response.json())
                smartcarttoken = response.json()['access_token']
                access_token = create_access_token(data={"sub": user[7]})
                query = ("UPDATE users SET token = %s WHERE username = %s")
                cursor.execute(query, (access_token, form_data.username))
                conn.commit()
            except  ValueError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
            return {"access_token": access_token, "token_type": "bearer", "smartcart_token": smartcarttoken}
        else :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")