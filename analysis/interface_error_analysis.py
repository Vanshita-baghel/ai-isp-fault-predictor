import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.data_loader import load_data
from utils.report_utils import save_csv
from utils.plotting import save_plot


df= load_data()

np.random.seed(42)

df["crc_errors"] = np.random.poisson(2, len(df))

df["input_errors"] = np.random.poisson(3, len(df))

df["output_errors"] = np.random.poisson(1, len(df))

df["total_interface_errors"] = df["crc_errors"] + df["input_errors"] + df["output_errors"]

error_stats= df.groupby("node_id")["total_interface_errors"].agg(mean_interface_errors="mean",
          max_interface_errors="max",
          min_interface_errors="min").round(2)

print(error_stats)

#worst router
worst_router= error_stats["mean_interface_errors"].idxmax()
print(worst_router)

router = "R01"

router_df = df[df["node_id"] == router]

save_plot(router_df["timestamp"], router_df["total_interface_errors"], f"Interface Errors - {router}", "Time", "Errors", f"{router}_interface_errors.png" )

# plt.figure(figsize=(12,5))

# plt.plot(
#     router_df["timestamp"],
#     router_df["total_interface_errors"]
# )

# plt.title(f"Interface Errors - {router}")

# plt.xlabel("Time")

# plt.ylabel("Errors")

# plt.grid(True)

# plt.savefig(
#     f"reports/plots/{router}_interface_errors.png"
# )

# plt.show()

error_stats.reset_index().to_csv("reports/interface_error_summary.csv", index=False)

# df.to_csv("data/network_metrics_clean.csv", index=False)

save_csv(df, "network_metrics_clean.csv")
