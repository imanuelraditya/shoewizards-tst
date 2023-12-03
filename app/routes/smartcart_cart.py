from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.products import Product
from ..database import cursor, conn
from ..oauth2 import get_current_user
import requests

router = APIRouter(
    prefix='/smartcart-cart',
    tags=['SmartCart Cart']
)

cart = {}

@router.get('/cart')
async def get_info_cart(user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/cart"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        print(headers)

        response = requests.get(url, headers=headers)
        return response.json()

@router.put('/cart')
async def assign_cart(user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/cart"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        response = requests.put(url, headers=headers)
        return response.json()
    
@router.post('/cart')
async def add_item_to_cart(id_product: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/cart"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "id_product": id_product
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
@router.delete('/cart')
async def delete_user_cart(user: Annotated[User, Depends(get_current_user)]):
    query = "SELECT * FROM users WHERE userid = %s"
    cursor.execute(query, (user[0],)) 
    result = cursor.fetchall()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    smartcarttoken = user[9]

    url = f"http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/cart" 

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + smartcarttoken
    }

    response = requests.delete(url, headers=headers)
    return response.json()