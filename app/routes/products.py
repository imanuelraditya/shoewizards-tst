from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.products import Product
from ..database import cursor, conn
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

products = {}

@router.get('/products')
async def read_all_products():
    query = ("SELECT * FROM products")
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@router.get('/products/{productid}')
async def read_product(productid: int):
    query = ("SELECT * FROM products WHERE productid = %s")
    cursor.execute(query, (productid,))
    result = cursor.fetchall()
    if result :
        return result
    else :
        return "Product ID "+str(productid)+" does not exist."
    
@router.post('/products')
async def add_product(producttype: str, productbrand: str, productcolor: str, productsize: int, productcondition: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM products")
    cursor.execute(query)
    result = cursor.fetchall()
    if not result :
        productid = 1
    else :
        query = ("SELECT MAX(productid) FROM products")
        cursor.execute(query)
        result = cursor.fetchall()
        productid = result[0][0] + 1

    query = ("INSERT INTO products (productid, producttype, productbrand, productcolor, productsize, productcondition) VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (productid, producttype, productbrand, productcolor, productsize, productcondition))
    conn.commit()
    return "Product ID "+str(productid)+" added."

@router.put('/products/{productid}')
async def update_product(productid: int, producttype: str, productbrand: str, productcolor: str, productsize: int, productcondition: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM products WHERE productid = %s")
    cursor.execute(query, (productid,))
    result = cursor.fetchall()
    if result :
        query = ("UPDATE products SET producttype = %s, productbrand = %s, productcolor = %s, productsize = %s, productcondition = %s WHERE productid = %s")
        cursor.execute(query, (producttype, productbrand, productcolor, productsize, productcondition, productid))
        conn.commit()
        return "Product ID "+str(productid)+" updated."
    else :
        return "Product ID "+str(productid)+" does not exist."
    
@router.delete('/products/{productid}')
async def delete_product(productid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM products WHERE productid = %s")
    cursor.execute(query, (productid,))
    result = cursor.fetchall()
    if result :
        query = ("DELETE FROM products WHERE productid = %s")
        cursor.execute(query, (productid,))
        conn.commit()
        return "Product ID "+str(productid)+" deleted."
    else :
        return "Product ID "+str(productid)+" does not exist."