import sys
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

from happy_computing import HappyComputingSimulation

# Run ONE simulation with detailed tracking
sim = HappyComputingSimulation(seed=42)
stats = sim.run_simulation(480)

print("=" * 70)
print("DEBUG: Verificar tipos de servicio")
print("=" * 70)
print(f"\nTotal de clientes: {len(stats.client_service_types)}")
print(f"Clientes servidos (stats): {stats.clients_served}")
print()

# Contar por tipo
type_counts = [0, 0, 0, 0]
for service_type in stats.client_service_types:
    type_counts[service_type] += 1

type_names = ['Reparación Garantía', 'Reparación Sin Garantía', 
             'Cambio de Equipo', 'Venta de Reparados']

print("Distribución de tipos de servicio:")
for idx, name in enumerate(type_names):
    print(f"  {name}: {type_counts[idx]} clientes")

print(f"\nTotal: {sum(type_counts)}")
print()

# Print stats by type
print("Stats por tipo:")
stats_by_type = stats.get_stats_by_service_type()
for name, data in stats_by_type.items():
    print(f"  {name}: {data['count']} clientes, ${data['total_profit']:.0f}")
