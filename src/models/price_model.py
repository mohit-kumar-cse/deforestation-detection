# C:\AgriPredict-AI\src\models\price_model.py
import pandas as pd
import numpy as np

import joblib

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)



# ==========================
# Load Dataset
# ==========================

df = pd.read_csv(
    "data/processed/price_features.csv"
)


print("Dataset Loaded")

print(df.head())



# ==========================
# Convert Date Removed
# ==========================

if "Price Date" in df.columns:

    df=df.drop(
        "Price Date",
        axis=1
    )



# ==========================
# Encode Categorical Columns
# ==========================


categorical_columns=[

    "STATE",
    "District Name",
    "Market Name",
    "Commodity",
    "Variety",
    "Grade"

]


encoders={}



for column in categorical_columns:


    encoder=LabelEncoder()


    df[column]=encoder.fit_transform(
        df[column]
    )


    encoders[column]=encoder



# Save encoders

joblib.dump(
    encoders,
    "models/price_encoders.pkl",
    compress=3
)



# ==========================
# Features and Target
# ==========================


X=df.drop(

    "Modal_Price",

    axis=1

)


y=df["Modal_Price"]



print("Feature Shape:")
print(X.shape)


print("Target Shape:")
print(y.shape)



# ==========================
# Train Test Split
# ==========================


X_train,X_test,y_train,y_test=train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)



# ==========================
# Models
# ==========================


models={


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



best_model=None

best_score=-999



results={}



for name,model in models.items():


    print("\nTraining:",name)


    model.fit(

        X_train,

        y_train

    )


    pred=model.predict(

        X_test

    )


    mae=mean_absolute_error(

        y_test,

        pred

    )


    rmse=np.sqrt(

        mean_squared_error(

            y_test,

            pred

        )

    )


    r2=r2_score(

        y_test,

        pred

    )


    print("MAE:",mae)

    print("RMSE:",rmse)

    print("R2:",r2)



    results[name]=r2



    if r2>best_score:

        best_score=r2

        best_model=model




# ==========================
# Save Best Model
# ==========================


joblib.dump(

    best_model,

    "models/price_forecasting_model.pkl"

)



print("\n================")

print("Best Price Model Saved")

print("================")


print(results)