import pandas as pd
import os
import matplotlib.pyplot as plt
from utils.data_loader import load_data
from utils.report_utils import save_csv
from utils.plotting import save_plot

df= load_data()

INTERFACE_CAPACITY= 1000    # assumption
df["bandwidth_utilization"]= (df["bandwidth_mbps"]/INTERFACE_CAPACITY)*100

bandwidth_stats= df.groupby("node_id")["bandwidth_utilization"].agg(mean_bandwidth="mean",
          max_bandwidth="max",
          min_bandwidth="min").round(2)

print(bandwidth_stats)

congested= bandwidth_stats[bandwidth_stats["mean_bandwidth"]>80]
print(congested)

peak= df.loc[df["bandwidth_utilization"].idxmax()]
print(f"peak - {peak}")

router= "R01"
router_df= df[df["node_id"]==router]

save_plot(router_df["timestamp"], router_df["bandwidth_utilization"], f"Bandwidth Utilization - {router}", "Time", "Utilization (%)", f"{router}_bandwidth.png" )

# plt.figure(figsize=(12,5))

# plt.plot(router_df["timestamp"], router_df["bandwidth_utilization"])

# plt.title(f"Bandwidth Utilization - {router}")

# plt.ylabel("Utilization (%)")

# plt.xlabel("Time")

# plt.grid(True)

# plt.show()

# plt.savefig(
#     f"reports/plots/{router}_bandwidth.png"
# )

# plt.close()


# bandwidth_stats.reset_index().to_csv(
#     "reports/bandwidth_summary.csv",
#     index=False
# )
save_csv(df, "bandwidth_summary.csv")
