# C:\AgriPredict-AI\api\routes\price_routes.py
from fastapi import APIRouter, HTTPException

from api.schemas import PriceRequest, PriceResponse
from src.prediction.price_predict import predict_price, get_options
from src.prediction.location_data import get_states, get_districts_for_state, get_markets_for_district

router = APIRouter()


@router.get("/options")
def options():
    return get_options()


@router.get("/states")
def states():
    return {"states": get_states()}


@router.get("/districts/{state}")
def districts(state: str):
    return {"districts": get_districts_for_state(state)}


@router.get("/markets/{district}")
def markets(district: str):
    return {"markets": get_markets_for_district(district)}


@router.post("/predict-price", response_model=PriceResponse)
def price_prediction(request: PriceRequest):
    try:
        result = predict_price(
            request.STATE,
            request.District,
            request.Market,
            request.Commodity,
            request.Variety,
            request.Grade,
            request.Year,
            request.Month,
            request.Day,
            request.Previous_Price,
            request.Price_7_Days_Ago,
            request.Price_30_Days_Ago
        )
        return {"predicted_price": float(result)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")