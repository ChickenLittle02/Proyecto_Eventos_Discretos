# Proyecto de Simulación de Eventos Discretos - Happy Computing

Este proyecto implementa una simulación de eventos discretos para el problema "Happy Computing" utilizando Python.

## Datos del estudiante

- Estudiante: Rubén Martínez Rojas
- Carrera: Ciencias de la Computación
- Grupo: C-311
- Problema asignado: #4 - Happy Computing

## Instalación

1. Instalar dependencias:
   pip install -r requirements.txt

## Uso

Ejecutar la simulación:

```bash
python src/main.py
```

Esto generará:

- `results/client_metrics.csv`
- `results/summary_metrics.csv`

## Opción B en curso

Se comenzó la implementación de la opción B con:

- exportación de métricas de clientes a CSV
- exportación de resumen de simulación a CSV
- análisis de colas con estadísticas de longitud máxima y promedio
- medición de utilización de recursos (vendedores, técnicos y técnico especializado)
- validación de la estructura de métricas en `src/stats.py`, incluyendo tiempos de llegada/salida y tiempos de espera/servicio
- ejecución de `src/main.py` para verificar la generación de `results/client_metrics.csv` y `results/summary_metrics.csv`
- creación de visualizaciones de análisis:
  - `results/happy_computing_analysis.png`
  - `results/service_type_analysis.png`
  - `results/queue_utilization_analysis.png`

## Uso de visualizaciones

Ejecutar las visualizaciones:

```bash
python src/visualizations.py
```

Esto generará gráficos de ganancias, distribución por tipo de servicio y análisis de colas/utilización.

## Estructura del proyecto

- src/: Código fuente
- results/: Resultados de simulaciones
- tests/: Pruebas
- informe/: Documentación
