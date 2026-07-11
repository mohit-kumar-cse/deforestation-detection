import pandas as pd
import joblib

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# Load data

df = pd.read_csv(
    "data/processed/yield_processed.csv"
)


# Split

X = df.drop(
    "hg/ha_yield",
    axis=1
)


y = df[
    "hg/ha_yield"
]


X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



# Load model

model = joblib.load(
    "models/yield_prediction_model.pkl"
)



# Prediction

prediction = model.predict(
    X_test
)



# Metrics

mae = mean_absolute_error(
    y_test,
    prediction
)


rmse = mean_squared_error(
    y_test,
    prediction
)**0.5


r2 = r2_score(
    y_test,
    prediction
)


print("Model Evaluation")
print("----------------")
print("MAE:",mae)
print("RMSE:",rmse)
print("R2 Score:",r2)



# Actual vs Prediction


import os


plt.figure(figsize=(8,6))


plt.scatter(
    y_test,
    prediction
)


plt.xlabel(
    "Actual Yield"
)


plt.ylabel(
    "Predicted Yield"
)


plt.title(
    "Actual vs Predicted Yield"
)


# create visualization folder if not exists

os.makedirs(
    "visualization",
    exist_ok=True
)


plt.savefig(
    "visualization/actual_vs_predicted.png"
)


print(
    "Graph saved successfully"
)