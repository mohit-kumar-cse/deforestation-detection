import pandas as pd



# ==========================
# Cleaning Function
# ==========================

def clean_data(df):


    # Remove duplicate rows

    df = df.drop_duplicates()



    # Remove unnecessary index column

    if "Unnamed: 0" in df.columns:

        df = df.drop(
            "Unnamed: 0",
            axis=1
        )



    # Handle missing values

    for column in df.columns:


        if df[column].isnull().sum() > 0:


            if df[column].dtype == "object":


                df[column] = df[column].fillna(

                    df[column].mode()[0]

                )


            else:


                df[column] = df[column].fillna(

                    df[column].mean()

                )


    return df





# ==========================
# Main Execution
# ==========================

if __name__ == "__main__":


    # Load raw dataset

    data = pd.read_csv(

        "data/raw/crop_yield_raw.csv"

    )



    print("Before Processing")

    print(data.head())



    print("\nShape Before:")

    print(data.shape)



    # Cleaning

    data = clean_data(data)



    print("\nAfter Processing")

    print(data.head())



    print("\nShape After:")

    print(data.shape)



    # Save cleaned dataset

    data.to_csv(

        "data/processed/yield_processed.csv",

        index=False

    )



    print(

        "\nProcessed dataset saved successfully"

    )