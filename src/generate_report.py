import os
import sys
import shutil
import subprocess
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ''))
from happy_computing import HappyComputingSimulation
from stats import Stats


TEX_TEMPLATE = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{caption}
\usepackage{float}
\usepackage{xcolor}
\title{Informe de Simulación - Happy Computing}
\author{Rubén Martínez Rojas \\ Ciencias de la Computación \\ Grupo C-311}
\date{\today}

\begin{document}
\maketitle

\section*{Datos del estudiante}
\begin{itemize}
  \item Estudiante: Rubén Martínez Rojas
  \item Carrera: Ciencias de la Computación
  \item Grupo: C-311
  \item Tema Seleccionado: \#4 - Happy Computing
  \item Orden del Problema: 4
\end{itemize}

\section{Introducción}
Este informe presenta los resultados de una simulación de eventos discretos para el problema ``Happy Computing'', un taller de reparación y venta de equipos informáticos. El objetivo es estimar la ganancia esperada en una jornada laboral de 8 horas, considerando múltiples tipos de servicios y recursos limitados.

\section{Descripción del sistema}
Happy Computing es un taller de reparaciones electrónicas. Las actividades realizadas son:
\begin{enumerate}
  \item Reparación por garantía (Gratis)
  \item Reparación fuera de garantía (\$350)
  \item Cambio de equipo (\$500)
  \item Venta de equipos reparados (\$750)
\end{enumerate}

El taller cuenta con tres tipos de empleados:
\begin{itemize}
  \item Vendedor
  \item Técnico
  \item Técnico especializado
\end{itemize}

Cuando un cliente llega, primero es atendido por un vendedor. Si el servicio requiere reparación (tipo 1 o 2), el cliente luego debe ser atendido por un técnico. Si el servicio es un cambio de equipo (tipo 3), el cliente debe ser atendido por un técnico especializado. Si todos los empleados que pueden atender al cliente están ocupados, se establece una cola para su servicio.

Un técnico especializado solo realizará reparaciones si no hay ningún cliente que desee un cambio de equipo en la cola.

El taller opera con:
\begin{itemize}
  \item 2 vendedores
  \item 3 técnicos ordinarios
  \item 1 técnico especializado
\end{itemize}

La jornada laboral se modela con una simulación de 8 horas (480 minutos).

\section{Modelo de simulación}
\begin{itemize}
  \item Llegadas: proceso de Poisson con tiempo entre llegadas exponencial de media 20 minutos.
  \item Tipo de servicio: probabilidades fijas por tipo.
  \item Atención de vendedor: distribución normal N(5, 2).
  \item Reparación por técnico ordinario: exponencial con media 20 minutos.
  \item Cambio de equipo por técnico especializado: exponencial con media 15 minutos.
\end{itemize}

Flujo de cliente:
\begin{itemize}
  \item Llegada $\rightarrow$ Vendedor $\rightarrow$ Técnico (si reparación) $\rightarrow$ Fin
  \item Llegada $\rightarrow$ Vendedor $\rightarrow$ Técnico especializado (si cambio de equipo) $\rightarrow$ Fin
\end{itemize}

\section{Resultados}
\subsection{Resumen de ganancias}
\begin{tabular}{lr}
\toprule
Métrica & Valor \\
\midrule
Promedio & \$ <<MEAN_PROFIT>> \\
Desv. estándar & \$ <<STD_PROFIT>> \\
IC 95\% & [\$ <<CI_LOW>> , \$ <<CI_HIGH>> ] \\
Mínimo & \$ <<MIN_PROFIT>> \\
Máximo & \$ <<MAX_PROFIT>> \\
Mediana & \$ <<MEDIAN_PROFIT>> \\
Q1 (25\%) & \$ <<Q1_PROFIT>> \\
Q3 (75\%) & \$ <<Q3_PROFIT>> \\
\bottomrule
\end{tabular}

\subsection{Clientes servidos}
\begin{tabular}{lr}
\toprule
Métrica & Valor \\
\midrule
Promedio & <<MEAN_CLIENTS>> \\
Desv. estándar & <<STD_CLIENTS>> \\
Mínimo & <<MIN_CLIENTS>> \\
Máximo & <<MAX_CLIENTS>> \\
Mediana & <<MEDIAN_CLIENTS>> \\
\bottomrule
\end{tabular}

\subsection{Análisis por tipo de servicio}
\begin{tabular}{lrrr}
\toprule
Tipo de servicio & Clientes & Porcentaje & Ganancia \\
\midrule
Reparación Garantía & <<TYPE_COUNT_0>> & <<TYPE_PCT_0>>\% & \$ <<TYPE_PROFIT_0>> \\
Reparación Sin Garantía & <<TYPE_COUNT_1>> & <<TYPE_PCT_1>>\% & \$ <<TYPE_PROFIT_1>> \\
Cambio de Equipo & <<TYPE_COUNT_2>> & <<TYPE_PCT_2>>\% & \$ <<TYPE_PROFIT_2>> \\
Venta de Reparados & <<TYPE_COUNT_3>> & <<TYPE_PCT_3>>\% & \$ <<TYPE_PROFIT_3>> \\
\bottomrule
\end{tabular}

\subsection{Estadísticas multi-run}
\begin{tabular}{lrrr}
\toprule
Métrica & Media & Desv. Est. & IC 95\% \\
\midrule
Ganancia promedio (\$) & \$ <<PROFIT_MEAN>> & \$ <<PROFIT_STD>> & [\$ <<PROFIT_CI_LOW>> , \$ <<PROFIT_CI_HIGH>> ] \\
Espera promedio (min) & <<WAIT_MEAN>> & <<WAIT_STD>> & [<<WAIT_CI_LOW>> , <<WAIT_CI_HIGH>> ] \\
Tiempo total promedio (min) & <<TOTAL_MEAN>> & <<TOTAL_STD>> & [<<TOTAL_CI_LOW>> , <<TOTAL_CI_HIGH>> ] \\
\bottomrule
\end{tabular}

\section{Visualizaciones}
<<FIGURES_SECTION>>

\section{Consideraciones de ejecución}
La generación del informe se realizó con <<NUM_RUNS>> corridas independientes de 480 minutos cada una. Cada ejecución usa una semilla distinta para asegurar independencia y reproducibilidad de los escenarios generados.

El análisis multi-run calcula medias muestrales, varianzas y el intervalo de confianza al 95\% para la ganancia, el tiempo de espera promedio y el tiempo total promedio en el sistema.

La gráfica de convergencia muestra cómo se estabiliza la estimación de la ganancia promedio a medida que aumentan las corridas.

Código fuente disponible en \url{<<GITHUB_URL>>}.

\section{Conclusiones}
A partir de <<NUM_RUNS>> simulaciones, la ganancia promedio por jornada de 8 horas se estimó en \$ <<MEAN_PROFIT>> con un intervalo de confianza del 95\% de [\$ <<CI_LOW>> , \$ <<CI_HIGH>> ]. El modelo permite estimar mejor la asignación de vendedores y técnicos para gestionar colas y mejorar la eficiencia operativa.

\end{document}
"""


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def save_profit_convergence_plot(profits, output_path):
    if len(profits) == 0:
        return
    cumulative_mean = np.cumsum(profits) / np.arange(1, len(profits) + 1)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4.5))
    plt.plot(cumulative_mean, marker='o', markersize=4, linewidth=1.5, label='Media acumulada de ganancia')
    plt.axhline(cumulative_mean[-1], color='red', linestyle='--', label=f'Media final $ {cumulative_mean[-1]:.2f}')
    plt.title('Convergencia de la ganancia promedio por corrida')
    plt.xlabel('Número de corrida')
    plt.ylabel('Ganancia promedio acumulada ($)')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


FIGURE_TEMPLATE = r"""
\begin{{figure}}[H]
\centering
\includegraphics[width=0.9\textwidth]{{{{{image_path}}}}}
\caption{{{{{caption}}}}}
\end{{figure}}
"""


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def make_figure_block(image_path, caption):
    return FIGURE_TEMPLATE.format(image_path=image_path, caption=caption)


def write_latex_file(output_path, content):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def compile_latex(tex_path, working_dir):
    command = ['pdflatex', '-interaction=batchmode', '-halt-on-error', os.path.basename(tex_path)]
    result = subprocess.run(command, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0, result.stdout.decode('utf-8', errors='ignore') + result.stderr.decode('utf-8', errors='ignore')


def generate_report(num_runs=100):
    base_dir = os.path.dirname(__file__)
    results_dir = os.path.abspath(os.path.join(base_dir, '..', 'results'))
    informe_dir = os.path.abspath(os.path.join(base_dir, '..', 'informe'))

    ensure_directory(results_dir)
    ensure_directory(informe_dir)

    print('=' * 70)
    print('GENERANDO INFORME LaTeX')
    print('=' * 70)

    profits = []
    clients_served = []
    all_stats = []

    print(f'Ejecutando {num_runs} simulaciones...')
    for i in range(num_runs):
        if (i + 1) % 25 == 0:
            print(f'  {i + 1}/{num_runs}...')
        sim = HappyComputingSimulation(seed=i)
        stats = sim.run_simulation(480)
        profits.append(stats.total_profit)
        clients_served.append(stats.clients_served)
        all_stats.append(stats)

    print(f'  {num_runs}/{num_runs} completadas')
    print()

    profits_array = np.array(profits, dtype=float)
    clients_array = np.array(clients_served, dtype=float)
    mean_profit = float(np.mean(profits_array))
    std_profit = float(np.std(profits_array, ddof=1)) if len(profits_array) > 1 else 0.0
    min_profit = float(np.min(profits_array))
    max_profit = float(np.max(profits_array))
    median_profit = float(np.median(profits_array))
    q1_profit = float(np.percentile(profits_array, 25))
    q3_profit = float(np.percentile(profits_array, 75))
    mean_clients = float(np.mean(clients_array))
    std_clients = float(np.std(clients_array, ddof=1)) if len(clients_array) > 1 else 0.0
    min_clients = float(np.min(clients_array))
    max_clients = float(np.max(clients_array))
    median_clients = float(np.median(clients_array))

    se_profit = std_profit / np.sqrt(num_runs) if num_runs > 0 else 0.0
    z_critical = 1.96
    ci_low = mean_profit - z_critical * se_profit
    ci_high = mean_profit + z_critical * se_profit

    avg_waits = np.array([stats.get_wait_time_stats()['mean'] for stats in all_stats], dtype=float)
    avg_total_times = np.array([stats.get_system_time_stats()['mean'] for stats in all_stats], dtype=float)

    profit_summary = Stats.sample_summary(profits, confidence=0.95)
    wait_summary = Stats.sample_summary(avg_waits.tolist(), confidence=0.95)
    total_time_summary = Stats.sample_summary(avg_total_times.tolist(), confidence=0.95)

    convergence_path = os.path.join(results_dir, 'multi_run_profit_convergence.png')
    save_profit_convergence_plot(profits, convergence_path)

    image_files = [
        'happy_computing_analysis.png',
        'service_type_analysis.png',
        'queue_evolution_analysis.png',
        'wait_time_vs_arrival.png',
        'multi_run_profit_convergence.png'
    ]

    for image in image_files:
        source = os.path.join(results_dir, image)
        destination = os.path.join(informe_dir, image)
        if os.path.exists(source):
            shutil.copy2(source, destination)

    figure_definitions = [
        (os.path.join(informe_dir, image_files[0]), 'Análisis global de ganancias y clientes.'),
        (os.path.join(informe_dir, image_files[1]), 'Distribución por tipo de servicio.'),
        (os.path.join(informe_dir, image_files[4]), 'Convergencia de la ganancia promedio en las corridas multi-run.'),
        (os.path.join(informe_dir, image_files[2]), 'Evolución de las colas en una corrida representativa.'),
        (os.path.join(informe_dir, image_files[3]), 'Tiempo de espera vs. tiempo de llegada en la corrida con mayor espera promedio.')
    ]

    figures_section = '\n'.join(
        make_figure_block(os.path.basename(path), caption)
        for path, caption in figure_definitions
        if os.path.exists(path)
    )

    if not figures_section:
        figures_section = 'No se encontraron imágenes de análisis para incluir en el informe.'

    service_stats = {
        'Reparación Garantía': {'count': 0, 'total_profit': 0.0},
        'Reparación Sin Garantía': {'count': 0, 'total_profit': 0.0},
        'Cambio de Equipo': {'count': 0, 'total_profit': 0.0},
        'Venta de Reparados': {'count': 0, 'total_profit': 0.0}
    }

    for stats_obj in all_stats:
        for key, value in stats_obj.get_stats_by_service_type().items():
            service_stats[key]['count'] += value['count']
            service_stats[key]['total_profit'] += value['total_profit']

    total_clients_all = sum(v['count'] for v in service_stats.values())
    type_counts = [service_stats[name]['count'] for name in service_stats]
    type_profits = [service_stats[name]['total_profit'] for name in service_stats]
    type_percentages = [100 * count / total_clients_all if total_clients_all > 0 else 0.0 for count in type_counts]

    tex_content = (
        TEX_TEMPLATE
        .replace('<<FIGURES_SECTION>>', figures_section)
        .replace('<<NUM_RUNS>>', str(num_runs))
        .replace('<<GITHUB_URL>>', 'https://github.com/ChickenLittle02/Proyecto_Eventos_Discretos')
        .replace('<<MEAN_PROFIT>>', f'{mean_profit:.2f}')
        .replace('<<STD_PROFIT>>', f'{std_profit:.2f}')
        .replace('<<CI_LOW>>', f'{ci_low:.2f}')
        .replace('<<CI_HIGH>>', f'{ci_high:.2f}')
        .replace('<<MIN_PROFIT>>', f'{min_profit:.2f}')
        .replace('<<MAX_PROFIT>>', f'{max_profit:.2f}')
        .replace('<<MEDIAN_PROFIT>>', f'{median_profit:.2f}')
        .replace('<<Q1_PROFIT>>', f'{q1_profit:.2f}')
        .replace('<<Q3_PROFIT>>', f'{q3_profit:.2f}')
        .replace('<<MEAN_CLIENTS>>', f'{mean_clients:.1f}')
        .replace('<<STD_CLIENTS>>', f'{std_clients:.2f}')
        .replace('<<MIN_CLIENTS>>', f'{min_clients:.0f}')
        .replace('<<MAX_CLIENTS>>', f'{max_clients:.0f}')
        .replace('<<MEDIAN_CLIENTS>>', f'{median_clients:.1f}')
        .replace('<<TYPE_COUNT_0>>', str(type_counts[0]))
        .replace('<<TYPE_PCT_0>>', f'{type_percentages[0]:.1f}')
        .replace('<<TYPE_PROFIT_0>>', f'{type_profits[0]:.0f}')
        .replace('<<TYPE_COUNT_1>>', str(type_counts[1]))
        .replace('<<TYPE_PCT_1>>', f'{type_percentages[1]:.1f}')
        .replace('<<TYPE_PROFIT_1>>', f'{type_profits[1]:.0f}')
        .replace('<<TYPE_COUNT_2>>', str(type_counts[2]))
        .replace('<<TYPE_PCT_2>>', f'{type_percentages[2]:.1f}')
        .replace('<<TYPE_PROFIT_2>>', f'{type_profits[2]:.0f}')
        .replace('<<TYPE_COUNT_3>>', str(type_counts[3]))
        .replace('<<TYPE_PCT_3>>', f'{type_percentages[3]:.1f}')
        .replace('<<TYPE_PROFIT_3>>', f'{type_profits[3]:.0f}')
        .replace('<<PROFIT_MEAN>>', f'{profit_summary["mean"]:.2f}')
        .replace('<<PROFIT_STD>>', f'{profit_summary["std"]:.2f}')
        .replace('<<PROFIT_CI_LOW>>', f'{profit_summary["ci_low"]:.2f}')
        .replace('<<PROFIT_CI_HIGH>>', f'{profit_summary["ci_high"]:.2f}')
        .replace('<<WAIT_MEAN>>', f'{wait_summary["mean"]:.2f}')
        .replace('<<WAIT_STD>>', f'{wait_summary["std"]:.2f}')
        .replace('<<WAIT_CI_LOW>>', f'{wait_summary["ci_low"]:.2f}')
        .replace('<<WAIT_CI_HIGH>>', f'{wait_summary["ci_high"]:.2f}')
        .replace('<<TOTAL_MEAN>>', f'{total_time_summary["mean"]:.2f}')
        .replace('<<TOTAL_STD>>', f'{total_time_summary["std"]:.2f}')
        .replace('<<TOTAL_CI_LOW>>', f'{total_time_summary["ci_low"]:.2f}')
        .replace('<<TOTAL_CI_HIGH>>', f'{total_time_summary["ci_high"]:.2f}')
    )

    tex_file = os.path.join(informe_dir, 'informe_happy_computing.tex')
    write_latex_file(tex_file, tex_content)

    success, log = compile_latex(tex_file, informe_dir)
    if success:
        print('✓ Informe PDF generado con LaTeX en:', os.path.join(informe_dir, 'informe_happy_computing.pdf'))
    else:
        print('Error al compilar LaTeX. Se generó el archivo .tex en:', tex_file)
        print(log)


if __name__ == '__main__':
    generate_report(num_runs=100)
