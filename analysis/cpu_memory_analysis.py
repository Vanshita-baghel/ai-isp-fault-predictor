# Plot CPU and memory utilization over time for one or two nodes.
# Compute per-node statistics:
# Mean CPU and memory utilization.
# Maximum CPU and memory utilization.
# Identify nodes whose average CPU or memory usage exceeds a threshold (for example, 80%).

# Save the plots and the summary table.

import pandas as pd
import matplotlib.pyplot as plt
import os

df= pd.read_csv("data/network_metrics.csv")
df["timestamp"]= pd.to_datetime(df["timestamp"])
print(df["timestamp"].dtype)

cpu_stats= df.groupby("node_id")["cpu_utilization"].agg(["mean", "min", "max"]).round(2)
memory_stats= df.groupby("node_id")["memory_utilization"].agg(["mean", "min", "max"])

report= cpu_stats.join(memory_stats, lsuffix="_cpu", rsuffix="_memory")

# print(report)

high_cpu= report[report["mean_cpu"]>80]
high_mem= report[report["mean_memory"]>80]

print(f"high usage cpu:\n {high_cpu}")
print(f"high usage memory:\n {high_mem}")

#plot cpu utilization of a particular router
router="R01"
router_df= df[df["node_id"]==router]

os.makedirs("reports/plots", exist_ok=True)

plt.figure(figsize=(12,5))
plt.plot(router_df["timestamp"], router_df["cpu_utilization"])

plt.xlabel("time")
plt.ylabel("cpu(%)")

plt.grid(True)

plt.title("CPU_UTILIZATION")

plt.savefig(f"reports/plots/{router}_cpu.png")

plt.show()


#plot memory utilization
plt.figure(figsize=(12,5))
plt.plot(router_df["timestamp"], router_df["memory_utilization"])

plt.xlabel("time")
plt.ylabel("memory(%)")

plt.grid(True)

plt.title(f"MEMORY_UTILIZATION - {router}" )

plt.savefig(f"reports/plots/{router}_memory.png")


plt.show()


report.to_csv("reports/cpu_memory_summary.csv")




