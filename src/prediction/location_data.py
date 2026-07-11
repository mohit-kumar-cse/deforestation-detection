# C:\AgriPredict-AI\src\prediction\location_data.py
import pandas as pd

_location_map = None


def _load_location_map():
    global _location_map

    if _location_map is not None:
        return _location_map

    df = pd.read_csv(
        "data/raw/crop_price_raw.csv",
        usecols=["STATE", "District Name", "Market Name"]
    )

    df = df.dropna()

    state_district_map = {}
    district_market_map = {}

    for state, group in df.groupby("STATE"):
        state_district_map[state] = sorted(group["District Name"].unique().tolist())

    for district, group in df.groupby("District Name"):
        district_market_map[district] = sorted(group["Market Name"].unique().tolist())

    _location_map = {
        "state_district_map": state_district_map,
        "district_market_map": district_market_map,
        "all_states": sorted(df["STATE"].unique().tolist())
    }

    return _location_map


def get_states():
    data = _load_location_map()
    return data["all_states"]


def get_districts_for_state(state):
    data = _load_location_map()
    return data["state_district_map"].get(state, [])


def get_markets_for_district(district):
    data = _load_location_map()
    return data["district_market_map"].get(district, [])