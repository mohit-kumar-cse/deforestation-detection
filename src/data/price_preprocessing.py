import pandas as pd



def clean_price_data(df):


    # Remove duplicates

    df = df.drop_duplicates()



    # Convert date

    df["Price Date"] = pd.to_datetime(
        df["Price Date"]
    )



    # Sort by date

    df = df.sort_values(
        "Price Date"
    )



    # Remove missing values

    df = df.dropna()



    return df





if __name__=="__main__":


    df = pd.read_csv(
        "data/raw/crop_price_raw.csv"
    )


    print("Before Cleaning")

    print(df.head())


    print(df.shape)



    df = clean_price_data(df)



    print("\nAfter Cleaning")

    print(df.head())


    print(df.shape)



    df.to_csv(

        "data/processed/price_processed.csv",

        index=False

    )


    print(
        "Price dataset processed successfully"
    )