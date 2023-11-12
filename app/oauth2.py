from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from . import database
from .models.tokendata import TokenData
from .password import verify_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='authentications/login')

SECRET_KEY = "*******************"
ALGORITHM = "********"
ACCESS_TOKEN_EXPIRE_MINUTES = "**"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta :
        expire = datetime.utcnow() + expires_delta
    else :
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    query = ("SELECT * FROM users WHERE username = %s")
    database.cursor.execute(query, (username,))
    result = database.cursor.fetchall()
    if not result :
        return False
    else :
        if verify_password(password, result[0][6]) :
            return result[0]
        else :
            return False

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    query = ("SELECT * FROM users WHERE username = %s")
    database.cursor.execute(query, (token_data.username,))
    result = database.cursor.fetchall()
    if not result :
        raise credentials_exception
    else :
        return result[0]