import sys
import os
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

from happy_computing import HappyComputingSimulation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Usar backend que no requiere display
matplotlib.use('Agg')


def create_visualizations(num_runs=100):
    """Crea visualizaciones de los resultados"""
    
    print("=" * 70)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 70)
    print()
    
    # Ejecutar simulaciones
    profits = []
    clients_served = []
    all_stats = []
    
    print("Ejecutando simulaciones...")
    for i in range(num_runs):
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{num_runs}...")
        
        sim = HappyComputingSimulation(seed=i)
        stats = sim.run_simulation(480)
        profits.append(stats.total_profit)
        clients_served.append(stats.clients_served)
        all_stats.append(stats)
    
    print(f"  {num_runs}/{num_runs} completadas")
    print()
    
    # Crear figura con múltiples subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Simulación de Happy Computing - 100 Runs', fontsize=16, fontweight='bold')
    
    # ========== Subplot 1: Histograma de Ganancias ==========
    ax = axes[0, 0]
    profits_array = np.array(profits)
    mean_profit = np.mean(profits_array)
    std_profit = np.std(profits_array, ddof=1)
    
    n, bins, patches = ax.hist(profits, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(mean_profit, color='red', linestyle='--', linewidth=2, label=f'Media: ${mean_profit:.0f}')
    ax.axvline(np.median(profits), color='green', linestyle='--', linewidth=2, label=f'Mediana: ${np.median(profits):.0f}')
    ax.set_xlabel('Ganancia ($)', fontsize=10)
    ax.set_ylabel('Frecuencia', fontsize=10)
    ax.set_title('Distribución de Ganancias por Jornada', fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # ========== Subplot 2: Boxplot de Ganancias ==========
    ax = axes[0, 1]
    box_data = ax.boxplot([profits], labels=['Ganancias'],patch_artist=True)
    box_data['boxes'][0].set_facecolor('lightblue')
    ax.set_ylabel('Ganancia ($)', fontsize=10)
    ax.set_title('Boxplot de Ganancias', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Agregar texto con estadísticas
    q25, q50, q75 = np.percentile(profits, [25, 50, 75])
    stats_text = f"Q1: ${q25:.0f}\nMediana: ${q50:.0f}\nQ3: ${q75:.0f}"
    ax.text(1.15, q50, stats_text, fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # ========== Subplot 3: Clientes Servidos ==========
    ax = axes[1, 0]
    clients_array = np.array(clients_served)
    mean_clients = np.mean(clients_array)
    
    n, bins, patches = ax.hist(clients_served, bins=15, color='lightgreen', edgecolor='black', alpha=0.7)
    ax.axvline(mean_clients, color='red', linestyle='--', linewidth=2, label=f'Media: {mean_clients:.1f}')
    ax.set_xlabel('Clientes Servidos', fontsize=10)
    ax.set_ylabel('Frecuencia', fontsize=10)
    ax.set_title('Distribución de Clientes Servidos por Jornada', fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # ========== Subplot 4: Tabla de Estadísticas ==========
    ax = axes[1, 1]
    ax.axis('off')
    
    # Calcular IC 95%
    from scipy import stats as scipy_stats
    se_profit = std_profit / np.sqrt(num_runs)
    z_critical = scipy_stats.norm.ppf(0.975)
    ci_low = mean_profit - z_critical * se_profit
    ci_high = mean_profit + z_critical * se_profit
    
    stats_text = f"""
    ESTADÍSTICAS GENERALES (100 Runs)
    
    GANANCIAS:
    • Promedio: ${mean_profit:.2f}
    • Desv. Est.: ${std_profit:.2f}
    • IC 95%: [${ci_low:.2f}, ${ci_high:.2f}]
    • Mín: ${np.min(profits):.2f}
    • Máx: ${np.max(profits):.2f}
    • Mediana: ${np.median(profits):.2f}
    
    CLIENTES:
    • Promedio: {mean_clients:.1f} clientes
    • Desv. Est.: {np.std(clients_array, ddof=1):.2f}
    • Rango: {np.min(clients_served):.0f} - {np.max(clients_served):.0f}
    """
    
    ax.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment='center',
            family='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout()

    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)

    output_path = os.path.join(results_dir, 'happy_computing_analysis.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Figura guardada: {output_path}")
    
    # ========== Gráfica adicional: Distribución por tipo de servicio ==========
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle('Análisis por Tipo de Servicio - 100 Runs', fontsize=16, fontweight='bold')
    
    # Contar por tipo de servicio
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
    
    type_names = ['Rep. Garantía', 'Rep. Sin Garantía', 'Cambio Equipo', 'Venta Reparados']
    
    # Gráfica 1: Distribución de clientes
    ax = axes2[0]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    wedges, texts, autotexts = ax.pie(total_by_type, labels=type_names, autopct='%1.1f%%',
                                       colors=colors, startangle=90)
    ax.set_title('Distribución de Clientes por Tipo de Servicio', fontweight='bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # Gráfica 2: Ganancias por tipo
    ax = axes2[1]
    bars = ax.bar(range(len(type_names)), profits_by_type, color=colors, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Tipo de Servicio', fontsize=10)
    ax.set_ylabel('Ganancia Total ($)', fontsize=10)
    ax.set_title('Ganancia Total por Tipo de Servicio (100 Runs)', fontweight='bold')
    ax.set_xticks(range(len(type_names)))
    ax.set_xticklabels(type_names, rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Agregar valores en las barras
    for i, (bar, profit) in enumerate(zip(bars, profits_by_type)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${profit/1000:.0f}K',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()

    output_path2 = os.path.join(results_dir, 'service_type_analysis.png')
    plt.savefig(output_path2, dpi=150, bbox_inches='tight')
    print(f"✓ Figura guardada: {output_path2}")

    # ========== Gráfica 3: Comparativa de colas y utilización ==========
    fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5))
    fig3.suptitle('Colas y Utilización de Recursos - 100 Runs', fontsize=16, fontweight='bold')

    seller_queue_means = [s.get_queue_statistics()['seller_queue']['mean'] for s in all_stats]
    technician_queue_means = [s.get_queue_statistics()['technician_queue']['mean'] for s in all_stats]
    specialized_queue_means = [s.get_queue_statistics()['specialized_queue']['mean'] for s in all_stats]

    queue_labels = ['Vendedores', 'Técnicos', 'Especializado']
    queue_means = [
        np.mean(seller_queue_means),
        np.mean(technician_queue_means),
        np.mean(specialized_queue_means)
    ]

    ax = axes3[0]
    bars = ax.bar(queue_labels, queue_means, color=['#4c72b0', '#55a868', '#c44e52'], edgecolor='black')
    ax.set_ylabel('Longitud media de cola', fontsize=10)
    ax.set_title('Cola promedio por tipo de servicio', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05, f'{height:.2f}', ha='center', va='bottom')

    if hasattr(all_stats[0], 'resource_utilization'):
        seller_utils = [s.resource_utilization['average_seller_utilization'] for s in all_stats]
        technician_utils = [s.resource_utilization['average_technician_utilization'] for s in all_stats]
        specialized_utils = [s.resource_utilization['specialized_utilization'] for s in all_stats]

        util_means = [
            np.mean(seller_utils),
            np.mean(technician_utils),
            np.mean(specialized_utils)
        ]

        ax = axes3[1]
        bars = ax.bar(queue_labels, util_means, color=['#8172b3', '#ccb974', '#64b5cd'], edgecolor='black')
        ax.set_ylabel('Utilización promedio', fontsize=10)
        ax.set_title('Utilización promedio de servidores', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        for bar, util in zip(bars, util_means):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.005, f'{height:.2%}', ha='center', va='bottom')
    else:
        axes3[1].axis('off')
        axes3[1].text(0.5, 0.5, 'No hay datos de utilización disponibles', ha='center', va='center', fontsize=12)

    fig3.tight_layout(rect=[0, 0, 1, 0.96])
    output_path3 = os.path.join(results_dir, 'queue_utilization_analysis.png')
    fig3.savefig(output_path3, dpi=150, bbox_inches='tight')
    print(f"✓ Figura guardada: {output_path3}")
    
    print()
    print("=" * 70)
    print("✅ VISUALIZACIONES COMPLETADAS")
    print("=" * 70)


if __name__ == '__main__':
    create_visualizations(num_runs=100)
