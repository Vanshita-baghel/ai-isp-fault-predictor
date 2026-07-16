import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_data
from utils.report_utils import save_csv


df= load_data()

df["ber"]= np.random.choice([1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4], size=len(df), p=[0.30, 0.25, 0.20, 0.15, 0.08, 0.02])

def classify_link_quality(ber):
    if ber<1e-9:
        return "Excellent"
    elif ber < 1e-6:
        return "Good"
    elif ber < 1e-4:
        return "Fair"
    else:
        return "Poor"


df["link_quality"]= df["ber"].apply(classify_link_quality)

#ber statistics by router
ber_stats = (df.groupby("node_id")["ber"].agg(mean_ber="mean",
          max_ber="max",
          min_ber="min").round(8))
print(ber_stats)

#count link quality levels
quality_counts= df["link_quality"].value_counts()
print(quality_counts)

#find worst router
worst_router= ber_stats["mean_ber"].idxmax()
print(f"worst Router: {worst_router}")

#visualize
router="R01"
router_df= df[df["node_id"]==router]

plt.figure(figsize=(12,5))

plt.plot(router_df["timestamp"], router_df["ber"])

plt.title(f"BER - {router}")

plt.xlabel("Time")

plt.ylabel("BER")

plt.grid(True)

plt.show()

ber_stats.reset_index().to_csv("reports/ber_summary.csv", index= False)

# df.to_csv(
#     "data/network_metrics_clean.csv",
#     index=False
# )
save_csv(df, "network_metrics_clean.csv")
