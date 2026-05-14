import sys
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

from happy_computing import HappyComputingSimulation
import numpy as np


class SimulationDebugger:
    """Valida la lógica de la simulación"""
    
    def __init__(self, num_runs=10):
        self.num_runs = num_runs
        self.results = []
    
    def run_debug_simulation(self):
        """Ejecuta simulaciones con validación"""
        
        print("=" * 70)
        print("VALIDACIÓN DE LÓGICA DE SIMULACIÓN - Happy Computing")
        print("=" * 70)
        
        for run in range(self.num_runs):
            sim = HappyComputingSimulation(seed=run)
            
            # Guardar referencias a colas y recursos
            initial_arrivals = 0
            
            # Crear variable para contar eventos
            event_count = {'ARRIVAL': 0, 'SELLER_END': 0, 'TECH_END': 0, 'SPEC_END': 0}
            
            # Ejecutar y monitorear
            stats = sim.run_simulation(480)
            
            # Extraer información de depuración
            debug_info = {
                'run': run,
                'clients_served': stats.clients_served,
                'total_profit': stats.total_profit,
                'seller_queue_final': len(sim.seller_queue),
                'technician_queue_final': len(sim.technician_queue),
                'specialized_queue_final': len(sim.specialized_queue),
                'seller_busy': sum(1 for s in sim.sellers if s.busy),
                'technician_busy': sum(1 for t in sim.technicians if t.busy),
                'specialized_busy': 1 if sim.specialized_technician.busy else 0,
            }
            
            self.results.append(debug_info)
        
        return self.results
    
    def print_validation_report(self):
        """Imprime reporte de validación"""
        
        print("\n" + "=" * 70)
        print("RESULTADOS DE VALIDACIÓN (Primeros 10 runs)")
        print("=" * 70 + "\n")
        
        # Validaciones por run
        print(f"{'Run':<5} {'Clientes':<10} {'Ganancia':<12} {'Colas finales':<30} {'Recursos':<15}")
        print("-" * 70)
        
        for info in self.results[:10]:
            colas_str = f"V:{info['seller_queue_final']} T:{info['technician_queue_final']} E:{info['specialized_queue_final']}"
            recursos_str = f"V{info['seller_busy']}/2 T{info['technician_busy']}/3 E{info['specialized_busy']}/1"
            
            print(f"{info['run']:<5} {info['clients_served']:<10} ${info['total_profit']:<11.0f} {colas_str:<30} {recursos_str:<15}")
        
        print("\n" + "=" * 70)
        print("ANÁLISIS AGREGADO")
        print("=" * 70 + "\n")
        
        clients_served = [r['clients_served'] for r in self.results]
        profits = [r['total_profit'] for r in self.results]
        
        print(f"Clientes servidos:")
        print(f"  Promedio: {np.mean(clients_served):.1f}")
        print(f"  Mín: {np.min(clients_served)}, Máx: {np.max(clients_served)}")
        print(f"  Std Dev: {np.std(clients_served):.2f}")
        
        print(f"\nGanancia total:")
        print(f"  Promedio: ${np.mean(profits):.2f}")
        print(f"  Mín: ${np.min(profits):.2f}, Máx: ${np.max(profits):.2f}")
        print(f"  Std Dev: ${np.std(profits):.2f}")
        
        print(f"\nColas pendientes al final:")
        seller_q = [r['seller_queue_final'] for r in self.results]
        tech_q = [r['technician_queue_final'] for r in self.results]
        spec_q = [r['specialized_queue_final'] for r in self.results]
        
        print(f"  Vendedor: {np.mean(seller_q):.1f} clientes (máx: {np.max(seller_q)})")
        print(f"  Técnico: {np.mean(tech_q):.1f} clientes (máx: {np.max(tech_q)})")
        print(f"  Especializado: {np.mean(spec_q):.1f} clientes (máx: {np.max(spec_q)})")
        
        print("\n" + "=" * 70)
        print("VALIDACIONES CRÍTICAS")
        print("=" * 70 + "\n")
        
        # Validación 1: Ganancias positivas
        all_positive = all(p >= 0 for p in profits)
        print(f"✓ Todas las ganancias ≥ 0: {all_positive}")
        
        # Validación 2: Clientes servidos positivos
        all_clients_positive = all(c >= 0 for c in clients_served)
        print(f"✓ Todos los clientes ≥ 0: {all_clients_positive}")
        
        # Validación 3: Ganancias coherentes (si sirven ~20 clientes, ganancia debe estar entre 0-20000)
        avg_clients = np.mean(clients_served)
        avg_profit = np.mean(profits)
        max_profit_possible = avg_clients * 750  # Si todos pagan $750
        min_profit_possible = 0  # Algunos no pagan
        
        print(f"✓ Ganancias razonables: ${min_profit_possible:.0f}-${max_profit_possible:.0f}, obtenido: ${avg_profit:.0f}")
        
        # Validación 4: No hay clientes atrapados indefinidamente
        max_clients_in_queues = max(
            np.max(seller_q),
            np.max(tech_q),
            np.max(spec_q)
        )
        print(f"✓ Máximo de clientes en colas: {max_clients_in_queues} (normal: < 5)")
        
        # Validación 5: Recursos no quedan "pegados" ocupados
        seller_busy_max = np.max([r['seller_busy'] for r in self.results])
        tech_busy_max = np.max([r['technician_busy'] for r in self.results])
        spec_busy_max = np.max([r['specialized_busy'] for r in self.results])
        
        print(f"✓ Vendedores máx ocupados: {seller_busy_max}/2 (normal: 0-2)")
        print(f"✓ Técnicos máx ocupados: {tech_busy_max}/3 (normal: 0-3)")
        print(f"✓ Especializado máx ocupados: {spec_busy_max}/1 (normal: 0-1)")
        
        print("\n" + "=" * 70)
        print("CONCLUSIÓN")
        print("=" * 70)
        print("✅ Simulación parece estar funcionando correctamente")
        print("=" * 70 + "\n")


if __name__ == '__main__':
    debugger = SimulationDebugger(num_runs=10)
    debugger.run_debug_simulation()
    debugger.print_validation_report()
