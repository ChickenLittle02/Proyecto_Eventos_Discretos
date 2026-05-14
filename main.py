import sys
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

from happy_computing import HappyComputingSimulation
import numpy as np

def main():
    # Run simulation multiple times for 8 hours (480 minutes)
    num_runs = 100
    all_stats = []

    print("=" * 70)
    print("EJECUTANDO 100 SIMULACIONES DE 8 HORAS CADA UNA")
    print("=" * 70)
    print()

    for i in range(num_runs):
        if (i + 1) % 20 == 0:
            print(f"  Completadas: {i + 1}/{num_runs} simulaciones...")
        
        sim = HappyComputingSimulation(seed=i)
        stats = sim.run_simulation(480)
        all_stats.append(stats)

    print(f"  Completadas: {num_runs}/{num_runs} simulaciones")
    print()

    # Estadísticas agregadas
    print("=" * 70)
    print("ESTADÍSTICAS AGREGADAS (100 RUNS)")
    print("=" * 70)
    print()

    # Extraer datos
    profits = [s.total_profit for s in all_stats]
    clients_served = [s.clients_served for s in all_stats]

    # Calcular intervalo de confianza
    profits_array = np.array(profits)
    n = len(profits_array)
    mean_profit = np.mean(profits_array)
    std_profit = np.std(profits_array, ddof=1)
    se_profit = std_profit / np.sqrt(n)
    
    from scipy import stats as scipy_stats
    z_critical = scipy_stats.norm.ppf(0.975)  # 95% CI
    ci_low = mean_profit - z_critical * se_profit
    ci_high = mean_profit + z_critical * se_profit

    print(f"💰 GANANCIAS POR JORNADA:")
    print(f"  Promedio: ${mean_profit:.2f}")
    print(f"  Desv. Estándar: ${std_profit:.2f}")
    print(f"  IC 95%: [${ci_low:.2f}, ${ci_high:.2f}]")
    print(f"  Mín: ${np.min(profits):.2f}")
    print(f"  Máx: ${np.max(profits):.2f}")
    print(f"  Mediana: ${np.median(profits):.2f}")
    print()

    clients_array = np.array(clients_served)
    print(f"👥 CLIENTES SERVIDOS POR JORNADA:")
    print(f"  Promedio: {np.mean(clients_array):.1f}")
    print(f"  Desv. Estándar: {np.std(clients_array, ddof=1):.2f}")
    print(f"  Rango: {np.min(clients_array):.0f} - {np.max(clients_array):.0f}")
    print()

    # Estadísticas agregadas por tipo de servicio
    total_by_type = [0, 0, 0, 0]
    profits_by_type = [0, 0, 0, 0]
    
    for stats_obj in all_stats:
        stats_by_type = stats_obj.get_stats_by_service_type()
        type_names = ['Reparación Garantía', 'Reparación Sin Garantía', 
                     'Cambio de Equipo', 'Venta de Reparados']
        
        for idx, name in enumerate(type_names):
            if name in stats_by_type:
                total_by_type[idx] += stats_by_type[name]['count']
                profits_by_type[idx] += stats_by_type[name]['total_profit']
    
    print("📈 POR TIPO DE SERVICIO (AGREGADO 100 RUNS):")
    type_names = ['Reparación Garantía', 'Reparación Sin Garantía', 
                 'Cambio de Equipo', 'Venta de Reparados']
    total_clients = sum(total_by_type)
    
    for idx, name in enumerate(type_names):
        pct = 100 * total_by_type[idx] / total_clients if total_clients > 0 else 0
        print(f"  {name}: {total_by_type[idx]} clientes ({pct:.1f}%), ${profits_by_type[idx]:.0f} ganancia")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()