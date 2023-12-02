from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.products import Product
from ..database import cursor, conn
from ..oauth2 import get_current_user
import requests

router = APIRouter(
    prefix='/transaction',
    tags=['Transaction']
)

transaction = {}

@router.get('/transaction')
async def get_information_transaction(name_product: str, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/detail_transaction/"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "name_product": name_product
        }

        response = requests.get(url, headers=headers, json=data)
        print(response.status_code)
        return response.json()

@router.get('/detail_transaction/{id_product}')
async def get_detail_transaction(id_product: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/detail_transaction/" + str(id_product)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "id_product": id_product
        }

        response = requests.get(url, headers=headers, json=data)
        print(response.status_code)

@router.post('/transaction')
async def create_transaction(user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/transaction"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        response = requests.post(url, headers=headers)
        return response.json()
        