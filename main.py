import sys
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

from happy_computing import HappyComputingSimulation
import numpy as np

def main():
    # Run simulation multiple times for 8 hours (480 minutes)
    num_runs = 100
    profits = []
    clients_served = []

    for i in range(num_runs):
        sim = HappyComputingSimulation(seed=i)
        stats = sim.run_simulation(480)
        profits.append(stats.total_profit)
        clients_served.append(stats.clients_served)

    avg_profit = np.mean(profits)
    std_profit = np.std(profits)
    avg_clients = np.mean(clients_served)
    std_clients = np.std(clients_served)

    print(f"After {num_runs} runs:")
    print(f"Average profit: ${avg_profit:.2f} ± ${std_profit:.2f}")
    print(f"Average clients served: {avg_clients:.2f} ± {std_clients:.2f}")

if __name__ == "__main__":
    main()