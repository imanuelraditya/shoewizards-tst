from pydantic import BaseModel

class Product(BaseModel):
    productid: int
    productname: str
    productdescription: str
    price: int
    stock: int
    producttype: str

    class Config:
        json_schema_extra = {
            "example": {
                "productid": 1,
                "productname": "Sneaker Deodorizer",
                "productdescription": "Eliminate odors and keep your sneakers smelling nice",
                "price": 129000,
                "stock": 50,
                "producttype": "Sneakers"
            }
        }

