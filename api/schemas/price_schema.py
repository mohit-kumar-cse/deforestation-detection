# C:\AgriPredict-AI\api\schemas\price_schema.py
from pydantic import BaseModel



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