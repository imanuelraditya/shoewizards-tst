from pydantic import BaseModel
from datetime import datetime

class Consultation(BaseModel):
    consultationid: int
    customerid: int
    shoeid: int
    productid: int
    consultdate: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "consultationid": 1,
                "customerid": 1,
                "shoeid": 1,
                "productid": 1,
                "consultdate": "2021-06-01 12:00:00"
            }
        }