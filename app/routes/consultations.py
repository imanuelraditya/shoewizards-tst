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
async def read_customer_consultations(userid: int, shoeid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[0] != userid :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not consult for other users")
    
    query = ("SELECT * FROM shoes WHERE shoeid = %s")
    cursor.execute(query, (shoeid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shoe not found.")
    elif result[0][6] != user[0] :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not consult for other users' shoes")
    
    query = ("SELECT * FROM consultations WHERE userid = %s AND shoeid = %s")
    cursor.execute(query, (userid, shoeid))
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
async def add_consultation(userid: int, shoeid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[0] != userid :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    
    query = ("SELECT * FROM shoes WHERE shoeid = %s")
    cursor.execute(query, (shoeid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shoe not found.")
    elif result[0][6] != user[0] :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You can not consult for other users' shoes")
    
    query = ("SELECT * FROM consultations WHERE userid = %s AND shoeid = %s")
    cursor.execute(query, (userid, shoeid))
    result = cursor.fetchall()
    if result :
        return "Consultation for User ID "+str(userid)+" and Shoe ID "+str(shoeid)+" exists."
    else :
        query = ("SELECT * FROM users WHERE userid = %s")
        cursor.execute(query, (userid,))
        result = cursor.fetchall()
        if not result :
            return "User ID "+str(userid)+" does not exist."
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
                        query = ("INSERT INTO consultations (consultationid, userid, shoeid, productid, consultdate) VALUES (%s, %s, %s, %s, %s)")
                        cursor.execute(query, (consultationid, userid, shoeid, productid, consultdate))
                        conn.commit()
                        consultationid += 1
                    return "Consultation for User ID "+str(userid)+" and Shoe ID "+str(shoeid)+" added."
                
@router.delete('/consultations/{consultationid}')
async def delete_consultation(consultationid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8].lower() != "admin" :
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