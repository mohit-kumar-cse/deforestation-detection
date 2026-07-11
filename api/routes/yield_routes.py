# C:\AgriPredict-AI\api\routes\yield_routes.py
from fastapi import APIRouter, HTTPException

from api.schemas import YieldRequest, YieldResponse
from src.prediction.predict import predict_yield, get_options

router = APIRouter()


@router.get("/options")
def options():
    return get_options()


@router.post("/predict", response_model=YieldResponse)
def predict(request: YieldRequest):
    try:
        result = predict_yield(
            request.Area,
            request.Item,
            request.Year,
            request.Rainfall,
            request.Pesticides,
            request.Temperature
        )
        return {"predicted_yield": result}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")