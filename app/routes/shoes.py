from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..models.shoes import Shoe
from ..database import cursor, conn
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/shoes',
    tags=['Shoes']
)

shoes = {}

@router.get('/shoes')
async def read_all_shoes():
    query = ("SELECT * FROM shoes")
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@router.get('/shoes/{shoeid}')
async def read_shoe(shoeid: int):
    query = ("SELECT * FROM shoes WHERE shoeid = %s")
    cursor.execute(query, (shoeid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shoe not found.")
    else :
        return result[0]

@router.post('/shoes')
async def add_shoe(shoetype: str, shoesize: str, shoecolor: str, shoebrand: str, initialcondition: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM shoes")
    cursor.execute(query)
    result = cursor.fetchall()
    if not result :
        shoeid = 1
    else :
        query = ("SELECT MAX(shoeid) FROM shoes")
        cursor.execute(query)
        result = cursor.fetchall()
        shoeid = result[0][0] + 1

    query = ("INSERT INTO shoes (shoeid, shoetype, shoesize, shoecolor, shoebrand, initialcondition) VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (shoeid, shoetype, shoesize, shoecolor, shoebrand, initialcondition))
    conn.commit()
    return "Shoe ID "+str(shoeid)+" added."

@router.put('/shoes/{shoeid}')
async def update_shoe(shoeid: int, shoetype: str, shoesize: str, shoecolor: str, shoebrand: str, initialcondition: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM shoes WHERE shoeid = %s")
    cursor.execute(query, (shoeid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shoe not found.")
    else :
        query = ("UPDATE shoes SET shoetype = %s, shoesize = %s, shoecolor = %s, shoebrand = %s, initialcondition = %s WHERE shoeid = %s")
        cursor.execute(query, (shoetype, shoesize, shoecolor, shoebrand, initialcondition, shoeid))
        conn.commit()
        return "Shoe ID "+str(shoeid)+" updated."
    
@router.delete('/shoes/{shoeid}')
async def delete_shoe(shoeid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM shoes WHERE shoeid = %s")
    cursor.execute(query, (shoeid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shoe not found.")
    else :
        query = ("DELETE FROM shoes WHERE shoeid = %s")
        cursor.execute(query, (shoeid,))
        conn.commit()
        return "Shoe ID "+str(shoeid)+" deleted."