import pandas as pd

def load_data(path="data/network_metrics_realistic.csv"):
    df= pd.read_csv(path)
    df["timestamp"]= pd.to_datetime(df["timestamp"])
    return df
    