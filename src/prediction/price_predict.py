# C:\AgriPredict-AI\src\prediction\price_predict.py
import joblib
import pandas as pd



# ==========================
# Load Model
# ==========================

model = joblib.load(
    "models/price_forecasting_model.pkl"
)



# ==========================
# Load Encoders
# ==========================

encoders = joblib.load(
    "models/price_encoders.pkl"
)



# ==========================
# Safe Encoder Function
# ==========================

def safe_encode(
        encoder,
        value
):

    if value in encoder.classes_:

        return encoder.transform(
            [value]
        )[0]

    else:

        print(
            f"Unknown value: {value}"
        )

        return -1


# ==========================
# Options Helper (for frontend dropdowns)
# ==========================

def get_options():
    return {
        "states": sorted(encoders["STATE"].classes_.tolist()),
        "districts": sorted(encoders["District Name"].classes_.tolist()),
        "markets": sorted(encoders["Market Name"].classes_.tolist()),
        "commodities": sorted(encoders["Commodity"].classes_.tolist()),
        "varieties": sorted(encoders["Variety"].classes_.tolist()),
        "grades": sorted(encoders["Grade"].classes_.tolist())
    }

# ==========================
# Prediction Function
# ==========================


def predict_price(
        state,
        district,
        market,
        commodity,
        variety,
        grade,
        year,
        month,
        day,
        previous_price,
        price_7_days,
        price_30_days
):


    data = {


        "STATE":
        safe_encode(
            encoders["STATE"],
            state
        ),


        "District Name":
        safe_encode(
            encoders["District Name"],
            district
        ),



        "Market Name":
        safe_encode(
            encoders["Market Name"],
            market
        ),



        "Commodity":
        safe_encode(
            encoders["Commodity"],
            commodity
        ),



        "Variety":
        safe_encode(
            encoders["Variety"],
            variety
        ),



        "Grade":
        safe_encode(
            encoders["Grade"],
            grade
        ),



        "Min_Price":
        previous_price,


        "Max_Price":
        previous_price,


        "Year":
        year,


        "Month":
        month,


        "Day":
        day,


        "DayOfWeek":
        0,


        "Previous_Price":
        previous_price,


        "Price_7_Days_Ago":
        price_7_days,


        "Price_30_Days_Ago":
        price_30_days

    }



    input_df = pd.DataFrame(
        [data]
    )



    prediction = model.predict(
        input_df
    )


    return prediction[0]





# ==========================
# Testing
# ==========================

if __name__=="__main__":


    result = predict_price(

        "Maharashtra",

        "nashik",

        "Lasalgaon(Niphad)",

        "Wheat",

        "Other",

        "FAQ",

        2026,

        7,

        8,

        2300,

        2200,

        2100

    )



    print(
        "Predicted Price:",
        result
    )