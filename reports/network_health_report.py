import pandas as pd

files= ["cpu_memory_summary.csv",

"bandwidth_summary.csv",

"ber_summary.csv",

"interface_error_summary.csv",

"latency_summary.csv"]

report= None

for file in files:
    df= pd.read_csv(f"reports/{file}")
    if report is None:
        report=df
    else:
        report= report.merge(df, on="node_id")

report.to_csv("reports/network_health_report.csv", index=False)

print(report.head())