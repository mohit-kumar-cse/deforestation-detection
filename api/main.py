# C:\AgriPredict-AI\api\main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.utils.model_loader import load_models
from api.routes.yield_routes import router as yield_router
from api.routes.price_routes import router as price_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_models()
    print("AI Models Loaded Successfully")

    yield

    # Shutdown (optional)
    # print("Shutting down...")


app = FastAPI(
    title="AgriPredict AI API",
    description="Crop Yield Prediction and Price Forecasting API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    yield_router,
    prefix="/yield",
    tags=["Yield Prediction"]
)

app.include_router(
    price_router,
    prefix="/price",
    tags=["Price Prediction"]
)


@app.get("/")
def home():
    return {
        "project": "AgriPredict AI",
        "status": "running",
        "message": "Crop Yield Prediction and Price Forecasting API"
    }