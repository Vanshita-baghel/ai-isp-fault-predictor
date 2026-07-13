import pandas as pd
import os
import matplotlib.pyplot as plt

df= pd.read_csv("data/network_metrics.csv")
df["timestamp"]= pd.to_datetime(df["timestamp"])
print(df["timestamp"].dtype)
INTERFACE_CAPACITY= 1000    # assumption
df["bandwidth_utilization"]= (df["bandwidth_mbps"]/INTERFACE_CAPACITY)*100

bandwidth_stats= df.groupby("node_id")["bandwidth_utilization"].agg(["mean", "min", "max"]).round(2)

print(bandwidth_stats)

congested= bandwidth_stats[bandwidth_stats["mean"]>80]
print(congested)

peak= df.loc[df["bandwidth_utilization"].idxmax()]
print(f"peak - {peak}")

router= "R01"
router_df= df[df["node_id"]==router]

plt.figure(figsize=(12,5))

plt.plot(router_df["timestamp"], router_df["bandwidth_utilization"])

plt.title(f"Bandwidth Utilization - {router}")

plt.ylabel("Utilization (%)")

plt.xlabel("Time")

plt.grid(True)

plt.show()

plt.savefig(
    f"reports/plots/{router}_bandwidth.png"
)

plt.close()


bandwidth_stats.reset_index().to_csv(
    "reports/bandwidth_summary.csv",
    index=False
)