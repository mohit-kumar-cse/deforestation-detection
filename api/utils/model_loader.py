# C:\AgriPredict-AI\api\utils\model_loader.py
import joblib


yield_model = None
price_model = None
price_encoders = None



def load_models():

    global yield_model
    global price_model
    global price_encoders


    if yield_model is None:

        yield_model = joblib.load(
            "models/yield_prediction_model.pkl"
        )


    if price_model is None:

        price_model = joblib.load(
            "models/price_forecasting_model.pkl"
        )


    if price_encoders is None:

        price_encoders = joblib.load(
            "models/price_encoders.pkl"
        )


    return {

        "yield_model":yield_model,

        "price_model":price_model,

        "price_encoders":price_encoders

    }