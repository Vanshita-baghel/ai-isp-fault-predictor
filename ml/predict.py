import joblib
import pandas as pd

model = joblib.load(
    "models/logistic_regression.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

df = pd.read_csv(
    "data/network_metrics_realistic.csv"
)

features = [
    "cpu_utilization",
    "memory_utilization",
    "bandwidth_utilization",
    "latency_ms",
    "ber",
    "packet_loss",
    "crc_errors",
    "input_errors",
    "output_errors",
]

X = scaler.transform(df[features])

df["predicted_failure"] = model.predict(X)

df["predicted_probability"] = model.predict_proba(X)[:, 1]

print(
    df[
        [
            "node_id",
            "timestamp",
            "predicted_failure",
            "predicted_probability",
        ]
    ].head()
)