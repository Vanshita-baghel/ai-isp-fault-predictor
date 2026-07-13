import pandas as pd

report= pd.read_csv("reports/cpu_memory_summary.csv")

print("=============CPU & MEMORY REPORT===============\n")
print(report)