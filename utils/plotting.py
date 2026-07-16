import matplotlib.pyplot as plt

import os

def save_plot(
        x,
        y,
        title,
        xlabel,
        ylabel,
        filename
):

    os.makedirs(
        "reports/plots",
        exist_ok=True
    )

    plt.figure(figsize=(12,5))

    plt.plot(x,y)

    plt.title(title)

    plt.xlabel(xlabel)

    plt.ylabel(ylabel)

    plt.grid(True)

    plt.savefig(
        f"reports/plots/{filename}"
    )

    plt.close()