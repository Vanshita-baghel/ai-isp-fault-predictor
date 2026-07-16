import os

def save_csv(df, filename):
    os.makedirs("reports", exist_ok=True)

    df.to_csv(
        f"reports/{filename}",
        index=False
    )