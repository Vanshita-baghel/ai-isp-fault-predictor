import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_data
from utils.report_utils import save_csv
from utils.plotting import save_plot

df= load_data()

df["total_interface_errors"]= df["crc_errors"]+df["input_errors"]+df["output_errors"]

def generate_fault_label(row):
    if (
        row["packet_loss"] > 5
        or row["latency_ms"] > 120
        or row["health_score"] < 60
        or row["total_interface_errors"] > 15
    ):
        return "Failure"

    elif (
        row["packet_loss"] > 2
        or row["latency_ms"] > 70
        or row["health_score"] < 75
    ):
        return "Warning"

    else:
        return "Healthy"
    

df["fault_label"]= df.apply(generate_fault_label, axis=1)

df["failure"]= (df["fault_label"]=="Failure").astype(int)

#simulate probability
df["failure_probability"] = ( df["packet_loss"]*5
                                + df["latency_ms"]/5
                                + df["cpu_utilization"]/10
)

df["failure_probability"] = df[
    "failure_probability"
].clip(
    0,
    100
)

#label summary
label_summary = df["fault_label"].value_counts().reset_index()

label_summary.columns = [
    "fault_label",
    "count"
]

print(label_summary)

#router summary
router_summary = (
    df.groupby("node_id")
      .agg(
          avg_failure_probability=(
              "failure_probability",
              "mean"
          ),
          failures=(
              "failure",
              "sum"
          )
      )
      .round(2)
      .reset_index()
)

print(router_summary)

save_csv(
    label_summary,
    "fault_label_summary.csv"
)

save_csv(
    router_summary,
    "failure_probability_summary.csv"
)

df.to_csv(
    "data/network_metrics_realistic.csv",
    index=False
)

router="R01"
router_df= df[df["node_id"]==router]

save_plot(router_df["timestamp"], router_df["failure_probability"], f"Failure Probability - {router}", "Time", "Probability (%)", f"{router}_failure_probability.png")

