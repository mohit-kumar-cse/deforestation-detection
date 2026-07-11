# C:\AgriPredict-AI\test_price.py
import requests
from src.prediction.price_predict import predict_price

# Get real valid options from the API
options = requests.get("http://127.0.0.1:8000/price/options").json()

state = options["states"][0]
district = options["districts"][0]
market = options["markets"][0]
commodity = options["commodities"][0]
variety = options["varieties"][0]
grade = options["grades"][0]

print("Using:", state, district, market, commodity, variety, grade)
print()

# Test 1 - baseline
r1 = predict_price(state, district, market, commodity, variety, grade, 2026, 7, 8, 2000, 1900, 1800)
print("Test 1 (Previous=2000):", r1)

# Test 2 - same everything, but very different price trend
r2 = predict_price(state, district, market, commodity, variety, grade, 2026, 7, 8, 3000, 2000, 1000)
print("Test 2 (Previous=3000):", r2)

# Test 3 - different commodity, same price trend as Test 1
if len(options["commodities"]) > 1:
    commodity2 = options["commodities"][1]
    r3 = predict_price(state, district, market, commodity2, variety, grade, 2026, 7, 8, 2000, 1900, 1800)
    print(f"Test 3 (Commodity={commodity2}, Previous=2000):", r3)