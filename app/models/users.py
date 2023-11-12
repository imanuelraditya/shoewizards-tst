from pydantic import BaseModel

class User(BaseModel):
    userid: int
    firstname: str
    lastname: str
    phonenumber: str
    address: str
    email: str
    password: str
    username: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "userid": 1,
                "firstname": "Imanuel",
                "lastname": "Raditya",
                "phonenumber": "112233445",
                "address": "Jl. Tubagus Ismail Depan",
                "email": "imanuelraditya@gmail.com",
                "password": "AJsanjASNJNj",
                "username": "imanuelraditya",
                "role": "Customer"
            }
        }
        