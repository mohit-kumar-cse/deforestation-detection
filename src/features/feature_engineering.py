import pandas as pd



def create_features(df):

    # Separate input and target

    X = df.drop(
        "hg/ha_yield",
        axis=1
    )


    y = df["hg/ha_yield"]


    return X, y



if __name__ == "__main__":


    df = pd.read_csv(
        "data/processed/yield_processed.csv"
    )


    X, y = create_features(df)


    print("Features:")
    print(X.head())


    print("\nTarget:")
    print(y.head())


    print("\nFeature Shape:")
    print(X.shape)


    print("\nTarget Shape:")
    print(y.shape)