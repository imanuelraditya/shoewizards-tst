from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import Annotated
from ..models.users import User
from ..models.consultations import Consultation
from ..database import cursor, conn
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/consultations',
    tags=['Consultations']
)

consultations = {}

@router.get('/consultations')
async def read_customer_consultations(customerid: int, shoeid: int):
    query = ("SELECT * FROM consultations WHERE customerid = %s AND shoeid = %s")
    cursor.execute(query, (customerid, shoeid))
    result = cursor.fetchall()
    if result :
        consultations = []
        for consultation in result:
            productid = consultation[3]
            query = ("SELECT * FROM products WHERE productid = %s")
            cursor.execute(query, (productid,))
            result = cursor.fetchall()
            if result :
                consultations.append(result[0][1])
            else :
                return "No matching products found."
        return "Based on your consultation, we recommend the following products: " + ", ".join(consultations)
    else :
        return "No matching consultations found."
    
@router.post('/consultations')
async def add_consultation(customerid: int, shoeid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM consultations WHERE customerid = %s AND shoeid = %s")
    cursor.execute(query, (customerid, shoeid))
    result = cursor.fetchall()
    if result :
        return "Consultation for Customer ID "+str(customerid)+" and Shoe ID "+str(shoeid)+" exists."
    else :
        query = ("SELECT * FROM customers WHERE customerid = %s")
        cursor.execute(query, (customerid,))
        result = cursor.fetchall()
        if not result :
            return "Customer ID "+str(customerid)+" does not exist."
        else :
            query = ("SELECT * FROM shoes WHERE shoeid = %s")
            cursor.execute(query, (shoeid,))
            result = cursor.fetchall()
            if not result :
                return "Shoe ID "+str(shoeid)+" does not exist."
            else :
                shoe_type = result[0][1]
                query = ("SELECT * FROM products WHERE producttype = %s")
                cursor.execute(query, (shoe_type,))
                result = cursor.fetchall()
                if not result :
                    return "No matching products found for the shoe type."
                else :
                    for product in result:
                        global consultationid
                        query = ("SELECT * FROM consultations")
                        cursor.execute(query)
                        result = cursor.fetchall()
                        if not result :
                            consultationid = 1
                        else :
                            query = ("SELECT MAX(consultationid) FROM consultations")
                            cursor.execute(query)
                            result = cursor.fetchall()
                            consultationid = result[0][0] + 1

                        productid = product[0]
                        consultdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        query = ("INSERT INTO consultations (consultationid, customerid, shoeid, productid, consultdate) VALUES (%s, %s, %s, %s, %s)")
                        cursor.execute(query, (consultationid, customerid, shoeid, productid, consultdate))
                        conn.commit()
                        consultationid += 1
                    return "Consultation for Customer ID "+str(customerid)+" and Shoe ID "+str(shoeid)+" added."
                
@router.delete('/consultations/{consultationid}')
async def delete_consultation(consultationid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM consultations WHERE consultationid = %s")
    cursor.execute(query, (consultationid,))
    result = cursor.fetchall()
    if result :
        query = ("DELETE FROM consultations WHERE consultationid = %s")
        cursor.execute(query, (consultationid,))
        conn.commit()
        return "Consultation ID "+str(consultationid)+" deleted."
    else :
        return "Consultation ID "+str(consultationid)+" does not exist."