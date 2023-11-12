from pydantic import BaseModel

class Shoe(BaseModel):
    shoeid: int
    shoetype: str
    shoesize: int
    shoecolor: str
    shoebrand: str
    initialcondition: str

    class Config:
        json_schema_extra = {
            "example": {
                "shoeid": 1,
                "shoetype": "Sneakers",
                "shoesize": 42,
                "shoecolor": "White",
                "shoebrand": "Nike",
                "initialcondition": "Fair"
            }
        }