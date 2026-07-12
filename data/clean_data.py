from temp import df
import pandas as pd

print(df.shape)

print(df.duplicated().sum())
print(df.isnull().sum())

print(df[df.duplicated(keep=False)])
df = df.drop_duplicates(subset=["node_id", "timestamp"], keep="first")
df = df.reset_index(drop=True)

res= df.groupby(["node_id", "status" ])["packet_loss"].mean().round(2)
res= df.groupby("node_id").agg({
    "packet_loss":["mean", "max"],
    "latency_ms":["mean"]
})
df["nodeid_mean_loss"]= df.groupby("node_id")["packet_loss"].transform("mean")
print(df)

# ---------------timestamp based operations;
print(df["timestamp"].dtype)
df["timestamp"] = pd.to_datetime(df["timestamp"])
print(df["timestamp"].dtype)

df["hour"]= df["timestamp"].dt.hour
print(df.head())

df.sort_values(["node_id", "timestamp"]).reset_index(drop=True)

df=df.drop_duplicates()