# C:\AgriPredict-AI\frontend\streamlit_app.py
import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AgriPredict AI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 AgriPredict AI")

st.caption(
    "AI-powered Crop Yield Prediction and Market Price Forecasting System"
)

st.write(
    "Crop Yield Prediction and Market Price Forecasting"
)


menu = st.sidebar.selectbox(
    "Choose Prediction",
    [
        "Yield Prediction",
        "Price Prediction"
    ]
)


# ========================
# Helper: fetch options with caching
# ========================

@st.cache_data(ttl=300)
def get_yield_options():
    response = requests.get(API_URL + "/yield/options", timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def get_price_options():
    response = requests.get(API_URL + "/price/options", timeout=10)
    response.raise_for_status()
    return response.json()


# ========================
# Yield Prediction
# ========================

if menu == "Yield Prediction":

    st.header("🌱 Crop Yield Prediction")

    st.info(
        "Select crop and environmental details to predict expected yield"
    )

    try:
        options = get_yield_options()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API. Make sure uvicorn is running on port 8000.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Could not load options from API: {e}")
        st.stop()

    area = st.selectbox("Area", options["areas"])
    crop = st.selectbox("Crop", options["crops"])

    year = st.number_input(
        "Year",
        min_value=1990,
        max_value=2030,
        value=2023
    )

    rainfall = st.number_input(
        "Average Rainfall (mm/year)",
        min_value=0.0,
        max_value=4000.0,
        value=1000.0,
        help="Average annual rainfall in millimeters"
    )

    pesticides = st.number_input(
        "Pesticides Used (tonnes)",
        min_value=0.0,
        value=500.0,
        help="Amount of pesticides used"
    )

    temperature = st.number_input(
        "Average Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=25.0
    )

    if st.button("🌾 Predict Yield"):

        try:
            response = requests.post(
                API_URL + "/yield/predict",
                json={
                    "Area": area,
                    "Item": crop,
                    "Year": year,
                    "Rainfall": rainfall,
                    "Pesticides": pesticides,
                    "Temperature": temperature
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            st.success(
                f"Predicted Yield: {result['predicted_yield']:.2f} hg/ha"
            )

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the API. Is uvicorn running?")

        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            st.error(f"❌ API Error ({response.status_code}): {detail}")

        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")


# ========================
# Price Prediction
# ========================

else:

    st.header("💰 Crop Price Prediction")

    try:
        states_data = requests.get(API_URL + "/price/states", timeout=10).json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API. Make sure uvicorn is running on port 8000.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Could not load states from API: {e}")
        st.stop()

    state = st.selectbox("State", states_data["states"])

    # Fetch districts for selected state
    try:
        districts_data = requests.get(API_URL + f"/price/districts/{state}", timeout=10).json()
    except Exception as e:
        st.error(f"❌ Could not load districts: {e}")
        st.stop()

    if not districts_data["districts"]:
        st.warning(f"No districts found for {state}")
        st.stop()

    district = st.selectbox("District", districts_data["districts"])

    # Fetch markets for selected district
    try:
        markets_data = requests.get(API_URL + f"/price/markets/{district}", timeout=10).json()
    except Exception as e:
        st.error(f"❌ Could not load markets: {e}")
        st.stop()

    if not markets_data["markets"]:
        st.warning(f"No markets found for {district}")
        st.stop()

    market = st.selectbox("Market", markets_data["markets"])

    price_options = get_price_options()

    commodity = st.selectbox("Commodity", price_options["commodities"])
    variety = st.selectbox("Variety", price_options["varieties"])
    grade = st.selectbox("Grade", price_options["grades"])

    price = st.number_input("Previous Price", min_value=0.0, value=2000.0)

    if st.button("Predict Price"):

        try:
            response = requests.post(
                API_URL + "/price/predict-price",
                json={
                    "STATE": state,
                    "District": district,
                    "Market": market,
                    "Commodity": commodity,
                    "Variety": variety,
                    "Grade": grade,
                    "Year": 2026,
                    "Month": 7,
                    "Day": 8,
                    "Previous_Price": price,
                    "Price_7_Days_Ago": price,
                    "Price_30_Days_Ago": price
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            st.success(
                f"Predicted Price: ₹ {result['predicted_price']:.2f}"
            )

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the API. Is uvicorn running?")

        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            st.error(f"❌ API Error ({response.status_code}): {detail}")

        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")