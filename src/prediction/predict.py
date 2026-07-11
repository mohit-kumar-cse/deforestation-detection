# C:\AgriPredict-AI\src\prediction\predict.py
import joblib
import pandas as pd


# ==========================
# Load Model
# ==========================

model = joblib.load("models/yield_prediction_model.pkl")


# ==========================
# Load Encoders
# ==========================

area_encoder = joblib.load("models/area_encoder.pkl")
crop_encoder = joblib.load("models/crop_encoder.pkl")


# ==========================
# Options Helper (for frontend dropdowns)
# ==========================

def get_options():
    return {
        "areas": sorted(area_encoder.classes_.tolist()),
        "crops": sorted(crop_encoder.classes_.tolist())
    }


# ==========================
# Prediction Function
# ==========================

def predict_yield(area, crop, year, rainfall, pesticides, temperature):

    # Validate Area
    if area not in area_encoder.classes_:
        raise ValueError(
            f"Unknown Area '{area}'. Please choose from the valid list of areas."
        )

    # Validate Crop
    if crop not in crop_encoder.classes_:
        raise ValueError(
            f"Unknown Crop '{crop}'. Please choose from the valid list of crops."
        )

    area_encoded = area_encoder.transform([area])[0]
    crop_encoded = crop_encoder.transform([crop])[0]

    input_data = pd.DataFrame({
        "Area": [area_encoded],
        "Item": [crop_encoded],
        "Year": [year],
        "average_rain_fall_mm_per_year": [rainfall],
        "pesticides_tonnes": [pesticides],
        "avg_temp": [temperature]
    })

    prediction = model.predict(input_data)

    return float(prediction[0])


# ==========================
# Testing
# ==========================

if __name__ == "__main__":
    result = predict_yield("India", "Wheat", 2026, 800, 2000, 25)
    print("Predicted Yield:", result, "hg/ha")