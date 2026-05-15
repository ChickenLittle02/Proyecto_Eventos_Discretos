import csv

SERVICE_TYPE_NAMES = [
    'Reparación Garantía',
    'Reparación Sin Garantía',
    'Cambio de Equipo',
    'Venta de Reparados'
]


def export_client_metrics(file_path, stats):
    """Exporta las métricas de cada cliente a un archivo CSV."""
    fieldnames = [
        'arrival_time',
        'departure_time',
        'service_type',
        'wait_time',
        'service_time',
        'total_time',
        'profit'
    ]

    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(stats.client_profits)):
            writer.writerow({
                'arrival_time': stats.client_arrival_times[i],
                'departure_time': stats.client_departure_times[i],
                'service_type': SERVICE_TYPE_NAMES[stats.client_service_types[i]],
                'wait_time': stats.client_wait_times[i],
                'service_time': stats.client_service_times[i],
                'total_time': stats.total_time_in_system[i],
                'profit': stats.client_profits[i]
            })


def export_summary(file_path, stats, utilization=None):
    """Exporta un resumen de la simulación a CSV."""
    queue_stats = stats.get_queue_statistics()

    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['metric', 'value'])
        writer.writerow(['total_profit', stats.total_profit])
        writer.writerow(['clients_served', stats.clients_served])
        writer.writerow(['avg_wait_time', stats.get_wait_time_stats()['mean']])
        writer.writerow(['avg_service_time', stats.get_service_time_stats()['mean']])
        writer.writerow(['avg_total_time', stats.get_system_time_stats()['mean']])
        writer.writerow(['seller_queue_mean', queue_stats['seller_queue']['mean']])
        writer.writerow(['seller_queue_max', queue_stats['seller_queue']['max']])
        writer.writerow(['technician_queue_mean', queue_stats['technician_queue']['mean']])
        writer.writerow(['technician_queue_max', queue_stats['technician_queue']['max']])
        writer.writerow(['specialized_queue_mean', queue_stats['specialized_queue']['mean']])
        writer.writerow(['specialized_queue_max', queue_stats['specialized_queue']['max']])

        if utilization is not None:
            writer.writerow(['avg_seller_utilization', utilization['average_seller_utilization']])
            writer.writerow(['avg_technician_utilization', utilization['average_technician_utilization']])
            writer.writerow(['specialized_utilization', utilization['specialized_utilization']])
