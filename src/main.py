from happy_computing import HappyComputingSimulation
import matplotlib.pyplot as plt

def main():
    # Run simulation for 8 hours (480 minutes)
    sim = HappyComputingSimulation(seed=42)
    stats = sim.run_simulation(480)

    print(f"Total profit: ${stats.total_profit}")
    print(f"Clients served: {stats.clients_served}")

    # Plot queue lengths over time (simplified, assuming we record at events)
    # For now, just print

if __name__ == "__main__":
    main()