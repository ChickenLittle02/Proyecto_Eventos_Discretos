import numpy as np


class Stats:
    def __init__(self):
        self.total_profit = 0
        self.clients_served = 0
        self.seller_queue_lengths = []
        self.technician_queue_lengths = []
        self.specialized_queue_lengths = []
        
        # Nuevas métricas por cliente
        self.client_wait_times = []      # Tiempo que esperan los clientes
        self.client_service_times = []   # Tiempo que tardan siendo atendidos
        self.client_profits = []         # Ganancia generada por cada cliente
        self.client_service_types = []   # Tipo de servicio de cada cliente
        self.total_time_in_system = []   # Tiempo total desde llegada hasta salida
        self.client_arrival_times = []   # Tiempo de llegada de cada cliente
        self.client_departure_times = [] # Tiempo de salida de cada cliente

    def add_profit(self, amount):
        self.total_profit += amount
        self.client_profits.append(amount)

    def increment_clients(self):
        self.clients_served += 1

    def record_queues(self, seller_q, tech_q, spec_q):
        self.seller_queue_lengths.append(len(seller_q))
        self.technician_queue_lengths.append(len(tech_q))
        self.specialized_queue_lengths.append(len(spec_q))
    
    def record_client_metrics(self, arrival_time, departure_time, wait_time, service_time, total_time, service_type):
        """Registra métricas de un cliente específico"""
        self.client_arrival_times.append(arrival_time)
        self.client_departure_times.append(departure_time)
        self.client_wait_times.append(wait_time)
        self.client_service_times.append(service_time)
        self.total_time_in_system.append(total_time)
        self.client_service_types.append(service_type)
    
    # ========== ESTADÍSTICAS DESCRIPTIVAS ==========
    
    def get_profit_stats(self):
        """Retorna estadísticas de ganancias"""
        profits = np.array(self.client_profits) if self.client_profits else np.array([0])
        
        return {
            'mean': np.mean(profits),
            'std': np.std(profits, ddof=1) if len(profits) > 1 else 0,
            'min': np.min(profits),
            'max': np.max(profits),
            'median': np.median(profits),
            'q25': np.percentile(profits, 25),
            'q75': np.percentile(profits, 75),
            'total': self.total_profit,
            'count': len(profits)
        }
    
    def get_wait_time_stats(self):
        """Retorna estadísticas de tiempos de espera"""
        wait_times = np.array(self.client_wait_times) if self.client_wait_times else np.array([0])
        
        return {
            'mean': np.mean(wait_times),
            'std': np.std(wait_times, ddof=1) if len(wait_times) > 1 else 0,
            'min': np.min(wait_times),
            'max': np.max(wait_times),
            'median': np.median(wait_times),
            'q25': np.percentile(wait_times, 25),
            'q75': np.percentile(wait_times, 75),
        }
    
    def get_service_time_stats(self):
        """Retorna estadísticas de tiempos de servicio"""
        service_times = np.array(self.client_service_times) if self.client_service_times else np.array([0])
        
        return {
            'mean': np.mean(service_times),
            'std': np.std(service_times, ddof=1) if len(service_times) > 1 else 0,
            'min': np.min(service_times),
            'max': np.max(service_times),
            'median': np.median(service_times),
        }
    
    def get_system_time_stats(self):
        """Retorna estadísticas de tiempo total en el sistema"""
        total_times = np.array(self.total_time_in_system) if self.total_time_in_system else np.array([0])
        
        return {
            'mean': np.mean(total_times),
            'std': np.std(total_times, ddof=1) if len(total_times) > 1 else 0,
            'min': np.min(total_times),
            'max': np.max(total_times),
        }
    
    def get_queue_statistics(self):
        """Retorna estadísticas de las longitudes de cola registradas"""
        def summarize(lengths):
            arr = np.array(lengths) if lengths else np.array([0])
            return {
                'mean': np.mean(arr),
                'max': np.max(arr),
                'median': np.median(arr),
                'count': len(arr)
            }

        return {
            'seller_queue': summarize(self.seller_queue_lengths),
            'technician_queue': summarize(self.technician_queue_lengths),
            'specialized_queue': summarize(self.specialized_queue_lengths),
        }
    
    @staticmethod
    def compute_confidence_interval(sample_values, confidence=0.95):
        """Calcula el intervalo de confianza para una muestra de valores."""
        values = np.array(sample_values, dtype=float) if len(sample_values) else np.array([0.0])
        n = len(values)
        mean = np.mean(values)
        if n < 2:
            return mean, mean

        std = np.std(values, ddof=1)
        se = std / np.sqrt(n)

        z_values = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.575
        }
        z_critical = z_values.get(confidence, 1.96)
        margin_of_error = z_critical * se

        return mean - margin_of_error, mean + margin_of_error

    @staticmethod
    def sample_summary(sample_values, confidence=0.95):
        """Retorna resumen estadístico de una muestra: media, varianza y CI."""
        values = np.array(sample_values, dtype=float) if len(sample_values) else np.array([0.0])
        n = len(values)
        mean = np.mean(values)
        std = np.std(values, ddof=1) if n > 1 else 0.0
        var = std ** 2
        ci_low, ci_high = Stats.compute_confidence_interval(values, confidence)

        return {
            'count': n,
            'mean': mean,
            'std': std,
            'var': var,
            'ci_low': ci_low,
            'ci_high': ci_high,
            'confidence': confidence
        }
    
    # ========== INTERVALO DE CONFIANZA ==========
    
    def get_profit_confidence_interval(self, confidence=0.95):
        """Calcula intervalo de confianza para ganancias promedio"""
        if not self.client_profits:
            return None, None
        
        profits = np.array(self.client_profits)
        n = len(profits)
        mean = np.mean(profits)
        std = np.std(profits, ddof=1)
        
        # Error estándar
        se = std / np.sqrt(n)
        
        # Valor crítico simple para intervalos comunes
        z_values = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.575
        }
        z_critical = z_values.get(confidence, 1.96)
        
        margin_of_error = z_critical * se
        
        return mean - margin_of_error, mean + margin_of_error
    
    # ========== ESTADÍSTICAS POR TIPO DE SERVICIO ==========
    
    def get_stats_by_service_type(self):
        """Retorna estadísticas separadas por tipo de servicio"""
        service_names = ['Reparación Garantía', 'Reparación Sin Garantía', 
                        'Cambio de Equipo', 'Venta de Reparados']
        
        stats_by_type = {}
        
        for service_type_id in range(4):
            profits_for_type = [
                self.client_profits[i] 
                for i in range(len(self.client_profits))
                if self.client_service_types[i] == service_type_id
            ]
            
            if profits_for_type:
                stats_by_type[service_names[service_type_id]] = {
                    'count': len(profits_for_type),
                    'total_profit': sum(profits_for_type),
                    'avg_profit': np.mean(profits_for_type),
                    'percentage': 100 * len(profits_for_type) / len(self.client_profits)
                }
        
        return stats_by_type
    
    # ========== RESUMEN COMPLETO ==========
    
    def print_summary(self, run_number=None):
        """Imprime un resumen completo de estadísticas"""
        print("\n" + "=" * 70)
        if run_number is not None:
            print(f"ESTADÍSTICAS - RUN #{run_number}")
        else:
            print("ESTADÍSTICAS DE SIMULACIÓN")
        print("=" * 70)
        
        profit_stats = self.get_profit_stats()
        wait_stats = self.get_wait_time_stats()
        service_stats = self.get_service_time_stats()
        system_stats = self.get_system_time_stats()
        
        print(f"\n📊 GANANCIAS:")
        print(f"  Total: ${profit_stats['total']:.2f}")
        print(f"  Promedio por cliente: ${profit_stats['mean']:.2f} ± ${profit_stats['std']:.2f}")
        print(f"  Rango: ${profit_stats['min']:.2f} - ${profit_stats['max']:.2f}")
        print(f"  Mediana: ${profit_stats['median']:.2f}")
        
        ci_low, ci_high = self.get_profit_confidence_interval()
        if ci_low is not None:
            print(f"  IC 95%: [${ci_low:.2f}, ${ci_high:.2f}]")
        
        print(f"\n👥 CLIENTES:")
        print(f"  Total atendidos: {profit_stats['count']}")
        
        print(f"\n⏱️  TIEMPOS DE ESPERA:")
        print(f"  Promedio: {wait_stats['mean']:.2f} min ± {wait_stats['std']:.2f} min")
        print(f"  Rango: {wait_stats['min']:.2f} - {wait_stats['max']:.2f} min")
        print(f"  Mediana: {wait_stats['median']:.2f} min")
        print(f"  Q25-Q75: {wait_stats['q25']:.2f} - {wait_stats['q75']:.2f} min")
        
        print(f"\n⏱️  TIEMPOS DE SERVICIO:")
        print(f"  Promedio: {service_stats['mean']:.2f} min ± {service_stats['std']:.2f} min")
        print(f"  Rango: {service_stats['min']:.2f} - {service_stats['max']:.2f} min")
        
        print(f"\n⏳ TIEMPO TOTAL EN SISTEMA:")
        print(f"  Promedio: {system_stats['mean']:.2f} min")
        print(f"  Rango: {system_stats['min']:.2f} - {system_stats['max']:.2f} min")
        
        queue_stats = self.get_queue_statistics()
        print(f"\n📌 ESTADÍSTICAS DE COLAS:")
        print(f"  Cola vendedores - promedio: {queue_stats['seller_queue']['mean']:.2f}, máximo: {queue_stats['seller_queue']['max']:.0f}")
        print(f"  Cola técnicos - promedio: {queue_stats['technician_queue']['mean']:.2f}, máximo: {queue_stats['technician_queue']['max']:.0f}")
        print(f"  Cola especializado - promedio: {queue_stats['specialized_queue']['mean']:.2f}, máximo: {queue_stats['specialized_queue']['max']:.0f}")
        
        print(f"\n📈 POR TIPO DE SERVICIO:")
        stats_by_type = self.get_stats_by_service_type()
        for service_name, stats_dict in stats_by_type.items():
            print(f"  {service_name}:")
            print(f"    Clientes: {stats_dict['count']} ({stats_dict['percentage']:.1f}%)")
            print(f"    Ganancia total: ${stats_dict['total_profit']:.2f}")
            print(f"    Ganancia promedio: ${stats_dict['avg_profit']:.2f}")
        
        print("\n" + "=" * 70)