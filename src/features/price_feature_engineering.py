import pandas as pd



# ==========================
# Load Data
# ==========================


df = pd.read_csv(

    "data/processed/price_processed.csv"

)



print("Original Data")

print(df.head())



# Convert Date

df["Price Date"] = pd.to_datetime(
    df["Price Date"]
)



# ==========================
# Time Features
# ==========================


df["Year"] = df["Price Date"].dt.year

df["Month"] = df["Price Date"].dt.month

df["Day"] = df["Price Date"].dt.day

df["DayOfWeek"] = df["Price Date"].dt.dayofweek



# ==========================
# Lag Features
# ==========================


# Sort data first

df = df.sort_values(
    "Price Date"
)



# Previous price

df["Previous_Price"] = (

    df["Modal_Price"]
    .shift(1)

)



# 7 days previous

df["Price_7_Days_Ago"] = (

    df["Modal_Price"]
    .shift(7)

)



# 30 days previous

df["Price_30_Days_Ago"] = (

    df["Modal_Price"]
    .shift(30)

)



# Remove missing lag rows

df = df.dropna()



print("\nAfter Feature Engineering")

print(df.head())



print("\nShape:")

print(df.shape)



# Save

df.to_csv(

    "data/processed/price_features.csv",

    index=False

)


print(
    "\nPrice Features Saved Successfully"
)