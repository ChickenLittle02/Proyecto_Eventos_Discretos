from happy_computing import HappyComputingSimulation
from stats import Stats
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')


def run_multi_run(num_runs=30, duration=480, seed_start=0):
    """Ejecuta varias corridas independientes y calcula estadísticas multi-run."""
    profits = []
    avg_waits = []
    avg_total_times = []

    for i in range(num_runs):
        sim = HappyComputingSimulation(seed=seed_start + i)
        stats = sim.run_simulation(duration)
        profits.append(stats.total_profit)
        avg_waits.append(stats.get_wait_time_stats()['mean'])
        avg_total_times.append(stats.get_system_time_stats()['mean'])

    profit_summary = Stats.sample_summary(profits, confidence=0.95)
    wait_summary = Stats.sample_summary(avg_waits, confidence=0.95)
    total_time_summary = Stats.sample_summary(avg_total_times, confidence=0.95)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    summary_path = os.path.join(RESULTS_DIR, 'multi_run_summary.csv')

    with open(summary_path, 'w', newline='') as file:
        file.write('metric,count,mean,std,var,ci_low,ci_high,confidence\n')
        file.write(f"profit,{profit_summary['count']},{profit_summary['mean']},{profit_summary['std']},{profit_summary['var']},{profit_summary['ci_low']},{profit_summary['ci_high']},{profit_summary['confidence']}\n")
        file.write(f"avg_wait,{wait_summary['count']},{wait_summary['mean']},{wait_summary['std']},{wait_summary['var']},{wait_summary['ci_low']},{wait_summary['ci_high']},{wait_summary['confidence']}\n")
        file.write(f"avg_total_time,{total_time_summary['count']},{total_time_summary['mean']},{total_time_summary['std']},{total_time_summary['var']},{total_time_summary['ci_low']},{total_time_summary['ci_high']},{total_time_summary['confidence']}\n")

    print(f"Multi-run summary written to {summary_path}")
    print("Profit summary:")
    print(profit_summary)
    print("Avg wait summary:")
    print(wait_summary)
    print("Avg total time summary:")
    print(total_time_summary)

    return {
        'profit_summary': profit_summary,
        'wait_summary': wait_summary,
        'total_time_summary': total_time_summary,
        'summary_path': summary_path
    }


if __name__ == '__main__':
    run_multi_run(num_runs=30, duration=480, seed_start=0)
