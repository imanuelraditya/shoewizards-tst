from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..models.users import User
from ..database import cursor, conn
from ..oauth2 import get_current_user
from ..password import hash_password

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

users = {}

@router.get('/users')
async def read_all_users(user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM users")
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@router.get('/users/{userid}')
async def read_user(userid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" and user[0] != userid :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to access this user.")
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (userid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        return result[0]

@router.post('/users')
async def register_user(firstname: str, lastname: str, phonenumber: str, address: str, email: str, password: str, username: str, role: str):
    query = ("SELECT * FROM users")
    cursor.execute(query)
    result = cursor.fetchall()
    if not result :
        userid = 1
    else :
        query = ("SELECT MAX(userid) FROM users")
        cursor.execute(query)
        result = cursor.fetchall()
        userid = result[0][0] + 1

    query = ("SELECT * FROM users WHERE email = %s")
    cursor.execute(query, (email,))
    result = cursor.fetchall()
    if result :
        return "Email "+email+" already exists."
    else :
        query = ("SELECT * FROM users WHERE username = %s")
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        if result :
            return "Username "+username+" already exists."
        else :
            query = ("INSERT INTO users (userid, firstname, lastname, phonenumber, address, email, password, username, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(query, (userid, firstname, lastname, phonenumber, address, email, hash_password(password), username, role))
            conn.commit()
            return "User ID "+str(userid)+" added."
        
@router.put('/users/{userid}')
async def update_user(userid: int, firstname: str, lastname: str, phonenumber: str, address: str, email: str, password: str, username: str, role: str, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin" and user[0] != userid :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update this user.")
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (userid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        query = ("SELECT * FROM users WHERE email = %s")
        cursor.execute(query, (email,))
        result = cursor.fetchall()
        if result :
            return "Email "+email+" already exists."
        else :
            query = ("SELECT * FROM users WHERE username = %s")
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            if result :
                return "Username "+username+" already exists."
            else :
                query = ("UPDATE users SET firstname = %s, lastname = %s, phonenumber = %s, address = %s, email = %s, password = %s, username = %s, role = %s WHERE userid = %s")
                cursor.execute(query, (firstname, lastname, phonenumber, address, email, hash_password(password), username, role, userid))
                conn.commit()
                return "User ID "+str(userid)+" updated."
            
@router.delete('/users/{userid}')
async def delete_user(userid: int, user: Annotated[User, Depends(get_current_user)]):
    if user[8] != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin.")
    query = ("SELECT * FROM users WHERE userid = %s")
    cursor.execute(query, (userid,))
    result = cursor.fetchall()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    else :
        query = ("DELETE FROM users WHERE userid = %s")
        cursor.execute(query, (userid,))
        conn.commit()
        return "User ID "+str(userid)+" deleted."