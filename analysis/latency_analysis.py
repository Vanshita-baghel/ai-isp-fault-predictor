import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/network_metrics_clean.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

np.random.seed(42)

df["latency_ms"] = np.random.normal(
    loc=30,
    scale=10,
    size=len(df)
)

df["latency_ms"] = df["latency_ms"].clip(lower=1)

def latency_status(latency):
    if latency < 20:
        return "Excellent"
    elif latency < 50:
        return "Good"
    elif latency < 100:
        return "Fair"
    else:
        return "Poor"

df["latency_status"] = df["latency_ms"].apply(latency_status)

latency_stats = (
    df.groupby("node_id")["latency_ms"]
      .agg(mean_latency="mean",
          max_latency="max",
          min_latency="min")
      .round(2)
)

print(latency_stats)

high_latency = latency_stats[
    latency_stats["mean_latency"] > 80
]

print(high_latency)

router = "R01"

router_df = df[df["node_id"] == router]

plt.figure(figsize=(12,5))

plt.plot(
    router_df["timestamp"],
    router_df["latency_ms"]
)

plt.title(f"Latency - {router}")

plt.xlabel("Time")

plt.ylabel("Latency (ms)")

plt.grid(True)

plt.savefig(
    f"reports/plots/{router}_latency.png"
)

plt.show()

latency_stats.reset_index().to_csv(
    "reports/latency_summary.csv",
    index=False
)

df.to_csv(
    "data/network_metrics_clean.csv",
    index=False
)