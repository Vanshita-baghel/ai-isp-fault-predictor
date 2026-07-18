import pandas as pd
from utils.data_loader import load_data
from utils.report_utils import save_csv
from utils.plotting import save_plot

df= load_data()

df["total_interface_errors"]= (df["crc_errors"]+ df["input_errors"]+ df["output_errors"])
#convert in range 0-1
df["cpu_norm"]= df["cpu_utilization"]/100
df["memory_norm"]= df["memory_utilization"]/100
df["bandwidth_norm"]= df["bandwidth_utilization"]/1000
df["latency_norm"]= df["latency_ms"]/100
df["packet_loss_norm"]= df["packet_loss"]/100
df["errors_norm"]= df["total_interface_errors"]/50

for col in ["cpu_norm", "memory_norm", "bandwidth_norm", "latency_norm", "packet_loss_norm", "errors_norm"]:
    df[col]= df[col].clip(0,1)

df["health_score"]= 100-(df["cpu_norm"]*20 + 
                         df["memory_norm"]*15 + 
                         df["bandwidth_norm"]*20 + 
                         df["latency_norm"]*20 + 
                         df["packet_loss_norm"]*15 + 
                         df["errors_norm"]*10  )

df["health_score"]= df["health_score"].round(2)

def classify_health(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Warning"
    else:
        return "Critical"

df["health_status"] = df["health_score"].apply(classify_health)

health_summary = (
    df.groupby("node_id")
      .agg(
          avg_health_score=("health_score", "mean"),
          min_health_score=("health_score", "min"),
          max_health_score=("health_score", "max"),
      )
      .round(2)
      .reset_index()
)

print(health_summary)

save_csv(health_summary, "health_score_summary.csv")

df.to_csv(
    "data/network_metrics_realistic.csv",
    index=False,
)

router = "R01"

router_df = df[df["node_id"] == router]


save_plot(router_df["timestamp"], router_df["health_score"], f"Health Score - {router}", "Time", "Health Score", f"{router}_health_score.png")
