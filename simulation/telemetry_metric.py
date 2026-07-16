import pandas as pd
import numpy as np


class TelemetryGenerator:
    """
    Generates realistic synthetic ISP telemetry data.
    """

    def __init__(
        self,
        routers=None,
        start_date="2026-01-01",
        periods=500,
        frequency="5min",
        random_seed=42,
    ):
        np.random.seed(random_seed)

        self.routers = routers or [
            "R01",
            "R02",
            "R03",
            "R04",
            "R05",
        ]

        self.timestamps = pd.date_range(
            start=start_date,
            periods=periods,
            freq=frequency,
        )

    # -----------------------------
    # Base Metrics
    # -----------------------------

    def generate_cpu(self):
        return np.clip(np.random.normal(45, 15), 5, 100)

    def generate_memory(self):
        return np.clip(np.random.normal(50, 12), 10, 100)

    def generate_bandwidth(self):
        return np.clip(np.random.normal(450, 150), 50, 1000)

    # -----------------------------
    # Correlated Metrics
    # -----------------------------

    def generate_latency(self, cpu, bandwidth):
        latency = (
            15
            + (cpu * 0.25)
            + (bandwidth / 120)
            + np.random.normal(0, 3)
        )

        return round(max(latency, 1), 2)

    def generate_ber(self, bandwidth):
        ber = (
            bandwidth / 1_000_000_000
        ) + np.random.uniform(
            0,
            2e-6,
        )

        return ber

    def generate_crc_errors(self, ber):
        lam = max(ber * 1_000_000, 0.2)
        return np.random.poisson(lam)

    def generate_input_errors(self, crc_errors):
        lam = max(crc_errors * 0.8, 0.5)
        return np.random.poisson(lam)

    def generate_output_errors(self):
        return np.random.poisson(1)

    def generate_packet_loss(self, latency, crc_errors):
        packet_loss = (
            latency / 200
            + crc_errors / 100
        )

        return round(
            np.clip(packet_loss, 0, 100),
            2,
        )

    # -----------------------------
    # Dataset Generation
    # -----------------------------

    def generate_dataset(self):

        rows = []

        for router in self.routers:

            for timestamp in self.timestamps:

                cpu = self.generate_cpu()

                memory = self.generate_memory()

                bandwidth = self.generate_bandwidth()

                latency = self.generate_latency(
                    cpu,
                    bandwidth,
                )

                ber = self.generate_ber(
                    bandwidth
                )

                crc_errors = self.generate_crc_errors(
                    ber
                )

                input_errors = self.generate_input_errors(
                    crc_errors
                )

                output_errors = self.generate_output_errors()

                packet_loss = self.generate_packet_loss(
                    latency,
                    crc_errors,
                )

                rows.append(
                    {
                        "timestamp": timestamp,
                        "node_id": router,
                        "cpu_utilization": round(cpu, 2),
                        "memory_utilization": round(memory, 2),
                        "bandwidth_utilization": round(
                            bandwidth, 2
                        ),
                        "latency_ms": latency,
                        "ber": ber,
                        "crc_errors": crc_errors,
                        "input_errors": input_errors,
                        "output_errors": output_errors,
                        "packet_loss": packet_loss,
                    }
                )

        return pd.DataFrame(rows)


def main():

    generator = TelemetryGenerator()

    df = generator.generate_dataset()

    df.to_csv(
        "data/network_metrics_realistic.csv",
        index=False,
    )

    print("=" * 60)
    print("Telemetry dataset generated successfully!")
    print("=" * 60)
    print(f"Rows      : {len(df)}")
    print(f"Routers   : {df['node_id'].nunique()}")
    print(
        f"Timestamps: {df['timestamp'].nunique()}"
    )
    print("=" * 60)

    print(df.head())


if __name__ == "__main__":
    main()