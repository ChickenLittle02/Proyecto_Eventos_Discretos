from happy_computing import HappyComputingSimulation
from export_data import export_client_metrics, export_summary
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    sim = HappyComputingSimulation(seed=42)
    duration = 480
    stats = sim.run_simulation(duration)

    utilization = sim.get_resource_utilization(duration)

    print(f"Total profit: ${stats.total_profit:.2f}")
    print(f"Clients served: {stats.clients_served}")
    print(f"Average seller utilization: {utilization['average_seller_utilization']:.2%}")
    print(f"Average technician utilization: {utilization['average_technician_utilization']:.2%}")
    print(f"Specialized technician utilization: {utilization['specialized_utilization']:.2%}")

    export_client_metrics(os.path.join(RESULTS_DIR, 'client_metrics.csv'), stats)
    export_summary(os.path.join(RESULTS_DIR, 'summary_metrics.csv'), stats, utilization)
    print(f"CSV export completed in {RESULTS_DIR}")


if __name__ == "__main__":
    main()