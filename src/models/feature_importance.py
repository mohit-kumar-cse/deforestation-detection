import pandas as pd
import joblib
import matplotlib.pyplot as plt

import os


# Load dataset

df = pd.read_csv(
    "data/processed/yield_processed.csv"
)


# Separate features

X = df.drop(
    "hg/ha_yield",
    axis=1
)



# Load trained model

model = joblib.load(
    "models/yield_prediction_model.pkl"
)



# Get feature importance

importance = model.feature_importances_



# Create dataframe

feature_importance = pd.DataFrame(
    {
        "Feature": X.columns,
        "Importance": importance
    }
)


# Sort values

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)


print(feature_importance)



# Create visualization folder

os.makedirs(
    "visualization",
    exist_ok=True
)



# Plot

plt.figure(figsize=(10,6))


plt.bar(
    feature_importance["Feature"],
    feature_importance["Importance"]
)


plt.xticks(
    rotation=45
)


plt.xlabel(
    "Features"
)


plt.ylabel(
    "Importance"
)


plt.title(
    "Feature Importance for Crop Yield Prediction"
)


plt.tight_layout()



plt.savefig(
    "visualization/feature_importance.png"
)


print(
    "Feature importance graph saved"
)