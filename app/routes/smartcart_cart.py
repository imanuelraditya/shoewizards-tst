from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.products import Product
from ..database import cursor, conn
from ..oauth2 import get_current_user
import requests
import json

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
        productquantitylist = []

        print(smartcarttoken)

        url = "https://smartcartchatbot.azurewebsites.net/cart"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        print(headers)

        response = requests.get(url, headers=headers)

        for inner_list in response.json():
            if len(inner_list) == 4:
                product_id = inner_list[2]

                url = "https://smartcartchatbot.azurewebsites.net/product/"

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + smartcarttoken
                }

                response = requests.get(url, headers=headers)

                if response.status_code == 200 :
                    products = response.json()
                    for product in products:
                        if product[0] == product_id :
                            productname = product[1]
                            price = product[2]
                            query = ("SELECT * FROM products WHERE productname = %s")
                            cursor.execute(query, (productname,))
                            result = cursor.fetchall()
                            if not result :
                                return "No matching products found."
                            else :
                                productdescription = result[0][2]
                                quantity = inner_list[3]
                                productquantitylist.append({"product_id": product_id, "productname": productname, "price": price, "productdescription": productdescription, "quantity": quantity})
        
        print(productquantitylist)
        return json.loads(json.dumps(productquantitylist))

@router.post('/cart_addproduct')
async def add_item_to_cart(id_product: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        url = "https://smartcartchatbot.azurewebsites.net/detail_cart"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "id_product": id_product,
            "addClick": 'true'
        }

        response = requests.post(url, headers=headers, params=data)
        return response.json()

@router.post('/cart_removeproduct')
async def remove_item_from_cart(id_product: int, user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        smartcarttoken = user[9]

        url = "https://smartcartchatbot.azurewebsites.net/detail_cart"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        data = {
            "id_product": id_product,
            "addClick": 'false'
        }

        response = requests.post(url, headers=headers, params=data)
        return response.json()