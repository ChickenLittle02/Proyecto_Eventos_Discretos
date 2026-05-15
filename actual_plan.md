Te propongo avanzar paso a paso así:

- Revisar y aprobar el nuevo flujo de exportación CSV en main.py y export_data.py. ✅
- Validar la estructura de métricas en stats.py. ✅
- Añadir análisis adicional de cola / utilización y posibles visualizaciones. ✅

Siguientes pasos para completar la Opción B:

- Agregar visualizaciones de evolución de colas a lo largo del tiempo.
- Generar gráficos de tiempos de espera vs. tiempo de llegada.
- Validar distribuciones con histogramas teóricos y Q-Q plots.
- Implementar análisis de sensibilidad variando el número de técnicos y vendedores.
- Extender el informe PDF para incluir todos los nuevos análisis y gráficos, incluyendo análisis multi-run y convergencia.
- Añadir el enlace al repositorio GitHub en README e informe.
- Incluir en el informe:
  - datos generales del estudiante
  - orden del problema asignado
  - ideas principales de solución
  - modelo de simulación de eventos discretos desarrollado
  - consideraciones obtenidas de las ejecuciones
- Implementar análisis estadístico multi-run:
  - calcular media muestral, varianza muestral y desviación estándar de la muestra
  - generar IC 95% para la ganancia promedio o tiempo promedio
  - opcional: criterio de parada por error estándar del estimador (capítulo 4)  - crear `src/multi_run.py` para ejecutar varias corridas independientes
  - generar `results/multi_run_summary.csv`- Opcional: exportar un CSV de resumen por corrida / multi-run para comparar resultados.
