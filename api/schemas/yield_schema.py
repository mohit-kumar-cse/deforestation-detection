# C:\AgriPredict-AI\api\schemas.py
from pydantic import BaseModel


class YieldRequest(BaseModel):

    Area: str

    Item: str

    Year: int

    Rainfall: float

    Pesticides: float

    Temperature: float



class YieldResponse(BaseModel):

    predicted_yield: float
    
    
    
    
class PriceRequest(BaseModel):

    STATE: str

    District: str

    Market: str

    Commodity: str

    Variety: str

    Grade: str

    Year: int

    Month: int

    Day: int

    Previous_Price: float

    Price_7_Days_Ago: float

    Price_30_Days_Ago: float



class PriceResponse(BaseModel):

    predicted_price: float    