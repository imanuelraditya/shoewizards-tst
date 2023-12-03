from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.products import Product
from ..database import cursor, conn
from ..oauth2 import get_current_user
import requests

router = APIRouter(
    prefix='/smartcart-product',
    tags=['SmartCart Product']
)

product = {}

@router.get('/product')
async def get_product(user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://localhost:3000/product"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        response = requests.get(url, headers=headers)
        return response.json()
    
@router.get('/product/{name_product}')
async def get_detail_product(name_product: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://localhost:3000/product/" + str(name_product)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        response = requests.get(url, headers=headers)
        return response.json()
    
@router.post('/product')
async def add_product(name_product: str, price: int, stock: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://localhost:3000/product"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "name_product": name_product,
            "price": price,
            "stock": stock
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
@router.put('/product/{id_product}')
async def update_product(id_product: int, name_product: str, price: int, stock: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://localhost:3000/product/" + str(id_product)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "name_product": name_product,
            "price": price,
            "stock": stock
        }

        response = requests.put(url, headers=headers, json=data)
        return response.json()
    
@router.delete('/product/{id_product}')
async def delete_product(id_product: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        print(smartcarttoken)

        url = "http://localhost:3000/product/" + str(id_product)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        response = requests.delete(url, headers=headers)
        return response.json()