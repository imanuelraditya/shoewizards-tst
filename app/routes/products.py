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
async def add_product(productname: str, productdescription: str, price: float, stock: int, producttype: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8].lower() != "admin" :
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

    if (producttype.lower() != "sneakers" and producttype.lower() != "loafers" and producttype.lower() != "flip-flops") :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product type must be either sneakers, loafers, or flip-flops.")
    
    query = ("INSERT INTO products (productid, productname, productdescription, price, stock, producttype) VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (productid, productname, productdescription, price, stock, producttype))
    conn.commit()
    return "Product ID "+str(productid)+" added."

@router.put('/products/{productid}')
async def update_product(productid: int, productname: str, productdescription: str, price: float, stock: int, producttype: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8].lower() != "admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM products WHERE productid = %s")
    cursor.execute(query, (productid,))
    result = cursor.fetchall()
    if result :
        if (producttype.lower() != "sneakers" and producttype.lower() != "loafers" and producttype.lower() != "flip-flops") :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product type must be either sneakers, loafers, or flip-flops.")
        
        query = ("UPDATE products SET productname = %s, productdescription = %s, price = %s, stock = %s, producttype = %s WHERE productid = %s")
        cursor.execute(query, (productname, productdescription, price, stock, producttype, productid))
        conn.commit()
        return "Product ID "+str(productid)+" updated."
    else :
        return "Product ID "+str(productid)+" does not exist."
    
@router.delete('/products/{productid}')
async def delete_product(productid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8].lower() != "admin" :
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