# C:\AgriPredict-AI\src\models\yield_model.py

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import joblib



# ==========================
# Load Dataset
# ==========================

df = pd.read_csv(
    "data/processed/yield_processed.csv"
)


print("Dataset Loaded")
print(df.head())



# ==========================
# Load Original Categorical Data
# ==========================

print("\nColumns:")
print(df.columns)



# ==========================
# Encoding
# ==========================

area_encoder = LabelEncoder()

crop_encoder = LabelEncoder()



# Encode Area

df["Area"] = area_encoder.fit_transform(
    df["Area"]
)


# Encode Crop(Item)

df["Item"] = crop_encoder.fit_transform(
    df["Item"]
)



# Save encoders

joblib.dump(
    area_encoder,
    "models/area_encoder.pkl"
)


joblib.dump(
    crop_encoder,
    "models/crop_encoder.pkl"
)


print("Encoders Saved")



# ==========================
# Features and Target
# ==========================


X = df.drop(
    "hg/ha_yield",
    axis=1
)


y = df[
    "hg/ha_yield"
]



print("\nFeatures")
print(X.head())


print("\nTarget")
print(y.head())



# ==========================
# Train Test Split
# ==========================


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)


print(
    "\nTraining:",
    X_train.shape
)


print(
    "Testing:",
    X_test.shape
)




# ==========================
# Models
# ==========================


models = {


"Linear Regression":

LinearRegression(),



"Random Forest":

RandomForestRegressor(
    n_estimators=50,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
),



"XGBoost":

XGBRegressor(

    n_estimators=200,

    learning_rate=0.05,

    max_depth=6,

    random_state=42

)


}




# ==========================
# Training
# ==========================


results={}


best_model=None

best_score=-999



for name,model in models.items():


    print("\nTraining:",name)



    model.fit(

        X_train,

        y_train

    )


    prediction=model.predict(

        X_test

    )



    mae=mean_absolute_error(

        y_test,

        prediction

    )



    rmse=np.sqrt(

        mean_squared_error(

            y_test,

            prediction

        )

    )



    r2=r2_score(

        y_test,

        prediction

    )



    results[name]=r2



    print("MAE:",mae)

    print("RMSE:",rmse)

    print("R2 Score:",r2)



    if r2 > best_score:


        best_score=r2

        best_model=model




# ==========================
# Save Best Model
# ==========================


joblib.dump(

    best_model,

    "models/yield_prediction_model.pkl",
    compress=3

)



print("\n====================")

print("Best Model Saved")

print("====================")



print(results)