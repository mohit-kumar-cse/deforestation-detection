import pandas as pd


def load_dataset(path):

    df = pd.read_csv(path)

    return df



if __name__ == "__main__":

    data = load_dataset(
        "data/raw/crop_yield_raw.csv"
    )

    print(data.head())