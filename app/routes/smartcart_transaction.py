from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.products import Product
from ..database import cursor, conn
from ..oauth2 import get_current_user
import requests
from typing import Optional
import json

router = APIRouter(
    prefix='/smartcart-transaction',
    tags=['SmartCart Transaction']
)

transaction = {}

@router.get('/transaction')
async def get_information_transaction(user: Annotated[User, Depends(get_current_user)]):
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (user[0],))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        username = user[7]
        smartcarttoken = user[9]

        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/transaction/" + username

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + smartcarttoken
        }

        response = requests.get(url, headers=headers)

        # return response.json()

        if response.status_code == 200 :
            for inner_list in response.json():
                transaction_id = inner_list[0]
                productquantitylist = []

                print(smartcarttoken)

                url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/detail_transaction/"

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + smartcarttoken
                }


                response = requests.get(url, headers=headers)

                # return response.json()
                
                for inner_list in response.json():
                    if transaction_id == inner_list[1]:
                        print(transaction_id)
                        product_id = inner_list[2]

                        url = "http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/product/"

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
                                    query = ("SELECT * FROM products WHERE productname = %s")
                                    cursor.execute(query, (productname,))
                                    result = cursor.fetchall()
                                    if not result :
                                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
                                    else :
                                        productquantitylist.append({"productname": productname, "quantity": inner_list[3]})
                        else :
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not get product.")
                
            print(productquantitylist)
            return json.loads(json.dumps(productquantitylist))


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
        