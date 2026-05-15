import sys
sys.path.append('/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src')

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib import colors
except ImportError:
    print("Error: reportlab no está instalado")
    print("Instala con: pip install reportlab")
    sys.exit(1)

import os
from happy_computing import HappyComputingSimulation
from stats import Stats
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def save_profit_convergence_plot(profits, output_path):
    if not profits:
        return

    cumulative_mean = np.cumsum(profits) / np.arange(1, len(profits) + 1)
    plt.figure(figsize=(8, 4.5))
    plt.plot(cumulative_mean, marker='o', markersize=4, linewidth=1.5, label='Media acumulada de ganancia')
    plt.axhline(cumulative_mean[-1], color='red', linestyle='--', label=f'Media final ${cumulative_mean[-1]:.2f}')
    plt.title('Convergencia de la ganancia promedio por corrida')
    plt.xlabel('Número de corrida')
    plt.ylabel('Ganancia promedio acumulada ($)')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def generate_report(num_runs=100):
    """Genera un informe PDF con los resultados de la simulación"""
    
    print("=" * 70)
    print("GENERANDO INFORME PDF")
    print("=" * 70)
    print()

    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    informe_dir = os.path.join(os.path.dirname(__file__), '..', 'informe')
    ensure_directory(results_dir)
    ensure_directory(informe_dir)
    
    # Ejecutar simulaciones
    print(f"Ejecutando {num_runs} simulaciones...")
    profits = []
    clients_served = []
    all_stats = []
    
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

    avg_waits = np.array([stats.get_wait_time_stats()['mean'] for stats in all_stats])
    avg_total_times = np.array([stats.get_system_time_stats()['mean'] for stats in all_stats])

    profit_summary = Stats.sample_summary(profits, confidence=0.95)
    wait_summary = Stats.sample_summary(avg_waits.tolist(), confidence=0.95)
    total_time_summary = Stats.sample_summary(avg_total_times.tolist(), confidence=0.95)

    convergence_path = os.path.join(results_dir, 'multi_run_profit_convergence.png')
    save_profit_convergence_plot(profits, convergence_path)
    
    # Crear documento
    output_pdf = os.path.join(informe_dir, 'informe_happy_computing.pdf')
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # ========== TÍTULO ==========
    story.append(Paragraph("INFORME DE SIMULACIÓN", title_style))
    story.append(Paragraph("Proyecto #4: Happy Computing", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    # Información del estudiante
    student_info = """
    <b>Estudiante:</b> Rubén Martínez Rojas<br/>
    <b>Carrera:</b> Ciencias de la Computación<br/>
    <b>Grupo:</b> C-311<br/>
    <b>Tema Seleccionado:</b> #4 - Happy Computing<br/>
    <b>Orden del Problema:</b> 4<br/>
    """
    story.append(Paragraph(student_info, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # ========== INTRODUCCIÓN ==========
    story.append(Paragraph("1. INTRODUCCIÓN", heading_style))
    intro_text = """
Este informe presenta los resultados de una simulación de eventos discretos para el problema 
"Happy Computing", un taller de reparación y venta de equipos informáticos. El objetivo es estimar 
la ganancia esperada en una jornada laboral de 8 horas, considerando múltiples tipos de servicios 
y recursos limitados.
    """
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # ========== DESCRIPCIÓN DEL SISTEMA ==========
    story.append(Paragraph("2. DESCRIPCIÓN DEL SISTEMA", heading_style))
    
    description_text = """
<b>Happy Computing</b> es un taller de reparaciones electrónicas. Las actividades 
realizadas son:
<br/>
1. Reparación por garantía (Gratis)
2. Reparación fuera de garantía ($350)
3. Cambio de equipo ($500)
4. Venta de equipos reparados ($750)
<br/><br/>
El taller cuenta con tres tipos de empleados:
<br/>
• Vendedor<br/>
• Técnico<br/>
• Técnico especializado
<br/><br/>
Cuando un cliente llega, primero es atendido por un vendedor. Si el servicio 
requiere reparación (tipo 1 o 2), el cliente luego debe ser atendido por un técnico. 
Si el servicio es un cambio de equipo (tipo 3), el cliente debe ser atendido por un 
técnico especializado. Si todos los empleados que pueden atender al cliente están 
ocupados, se establece una cola para su servicio.
<br/><br/>
Un técnico especializado solo realizará reparaciones si no hay ningún cliente que 
desee un cambio de equipo en la cola.
<br/><br/>
La simulación considera el siguiente escenario:
<br/>
• 2 vendedores<br/>
• 3 técnicos<br/>
• 1 técnico especializado
<br/>
La jornada laboral se modela como una simulación de 8 horas (480 minutos).
    """
    story.append(Paragraph(description_text, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # ========== MODELO DE SIMULACIÓN ==========
    story.append(Paragraph("3. MODELO DE SIMULACIÓN", heading_style))
    
    model_text = """
<b>Generación de llegadas:</b> Se usa un proceso de Poisson con intervalo 
de tiempo exponencial de media 20 minutos.<br/>
<b>Tipo de servicio:</b> Probabilidades definidas como:<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;- Tipo 1 (Reparación garantía): 0.45<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;- Tipo 2 (Reparación fuera de garantía): 0.25<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;- Tipo 3 (Cambio de equipo): 0.10<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;- Tipo 4 (Venta de reparados): 0.20<br/>
<b>Atención de vendedor:</b> Distribución normal N(5 min, 2 min).<br/>
<b>Reparación por técnico:</b> Exponencial con media 20 minutos.<br/>
<b>Cambio de equipo especializado:</b> Exponencial con media 15 minutos.<br/>
<br/>
<b>Flujo de cliente:</b><br/>
Llegada → Vendedor → (Técnico Ordinario si es reparación) → Fin<br/>
                         → (Técnico Especializado si es cambio de equipo) → Fin
    """
    story.append(Paragraph(model_text, body_style))
    story.append(PageBreak())
    
    # ========== RESULTADOS ==========
    story.append(Paragraph("4. RESULTADOS", heading_style))
    
    profits_array = np.array(profits)
    clients_array = np.array(clients_served)
    mean_profit = np.mean(profits_array)
    std_profit = np.std(profits_array, ddof=1)
    se_profit = std_profit / np.sqrt(num_runs)
    z_critical = scipy_stats.norm.ppf(0.975)
    ci_low = mean_profit - z_critical * se_profit
    ci_high = mean_profit + z_critical * se_profit
    
    story.append(Paragraph("4.1 Estadísticas de Ganancia", styles['Heading3']))
    
    # Tabla de ganancias
    data_profit = [
        ['Métrica', 'Valor'],
        ['Promedio', f'${mean_profit:.2f}'],
        ['Desv. Estándar', f'${std_profit:.2f}'],
        ['IC 95%', f'[${ci_low:.2f}, ${ci_high:.2f}]'],
        ['Mínimo', f'${np.min(profits):.2f}'],
        ['Máximo', f'${np.max(profits):.2f}'],
        ['Mediana', f'${np.median(profits):.2f}'],
        ['Q1 (25%)', f'${np.percentile(profits, 25):.2f}'],
        ['Q3 (75%)', f'${np.percentile(profits, 75):.2f}'],
    ]
    
    table_profit = Table(data_profit, colWidths=[2.5*inch, 2.5*inch])
    table_profit.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table_profit)
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("4.2 Estadísticas de Clientes", styles['Heading3']))
    
    # Tabla de clientes
    data_clients = [
        ['Métrica', 'Valor'],
        ['Promedio', f'{np.mean(clients_array):.1f}'],
        ['Desv. Estándar', f'{np.std(clients_array, ddof=1):.2f}'],
        ['Mínimo', f'{np.min(clients_served):.0f}'],
        ['Máximo', f'{np.max(clients_served):.0f}'],
        ['Mediana', f'{np.median(clients_served):.1f}'],
    ]
    
    table_clients = Table(data_clients, colWidths=[2.5*inch, 2.5*inch])
    table_clients.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table_clients)
    story.append(Spacer(1, 0.15*inch))
    
    # ========== ANÁLISIS POR TIPO DE SERVICIO ==========
    story.append(Paragraph("4.3 Distribución por Tipo de Servicio", styles['Heading3']))
    
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
    
    total_clients_all = sum(total_by_type)
    
    data_service = [
        ['Tipo de Servicio', 'Clientes', '%', 'Ganancia'],
        ['Reparación Garantía', f'{total_by_type[0]}', 
         f'{100*total_by_type[0]/total_clients_all:.1f}%', f'${profits_by_type[0]:.0f}'],
        ['Reparación Sin Garantía', f'{total_by_type[1]}', 
         f'{100*total_by_type[1]/total_clients_all:.1f}%', f'${profits_by_type[1]:.0f}'],
        ['Cambio de Equipo', f'{total_by_type[2]}', 
         f'{100*total_by_type[2]/total_clients_all:.1f}%', f'${profits_by_type[2]:.0f}'],
        ['Venta de Reparados', f'{total_by_type[3]}', 
         f'{100*total_by_type[3]/total_clients_all:.1f}%', f'${profits_by_type[3]:.0f}'],
    ]
    
    table_service = Table(data_service, colWidths=[2.0*inch, 1.2*inch, 1.0*inch, 1.3*inch])
    table_service.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table_service)
    
    story.append(Paragraph("4.4 Estadísticas Multi-Run", styles['Heading3']))
    data_multi = [
        ['Métrica', 'Media', 'Desv. Estándar', 'IC 95%'],
        ['Ganancia promedio ($)', f'${profit_summary["mean"]:.2f}', f'${profit_summary["std"]:.2f}',
         f'[${profit_summary["ci_low"]:.2f}, ${profit_summary["ci_high"]:.2f}]'],
        ['Espera promedio (min)', f'{wait_summary["mean"]:.2f}', f'{wait_summary["std"]:.2f}',
         f'[{wait_summary["ci_low"]:.2f}, {wait_summary["ci_high"]:.2f}]'],
        ['Tiempo total promedio (min)', f'{total_time_summary["mean"]:.2f}', f'{total_time_summary["std"]:.2f}',
         f'[{total_time_summary["ci_low"]:.2f}, {total_time_summary["ci_high"]:.2f}]'],
    ]
    table_multi = Table(data_multi, colWidths=[2.0*inch, 1.5*inch, 1.5*inch, 2.0*inch])
    table_multi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table_multi)
    story.append(PageBreak())
    
    # ========== GRÁFICAS ==========
    story.append(Paragraph("5. VISUALIZACIONES", heading_style))
    
    story.append(Paragraph("5.1 Análisis de Ganancias", styles['Heading3']))
    image_path_1 = os.path.join(results_dir, 'happy_computing_analysis.png')
    if os.path.exists(image_path_1):
        story.append(Image(image_path_1, width=6*inch, height=4.5*inch))
    else:
        story.append(Paragraph("(Imagen no disponible)", body_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    story.append(Paragraph("5.2 Análisis por Tipo de Servicio", styles['Heading3']))
    image_path_2 = os.path.join(results_dir, 'service_type_analysis.png')
    if os.path.exists(image_path_2):
        story.append(Image(image_path_2, width=6*inch, height=2.5*inch))
    else:
        story.append(Paragraph("(Imagen no disponible)", body_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("5.3 Convergencia de la Ganancia Promedio", styles['Heading3']))
    if os.path.exists(convergence_path):
        story.append(Image(convergence_path, width=6*inch, height=4.5*inch))
    else:
        story.append(Paragraph("(Imagen de convergencia no disponible)", body_style))
    
    story.append(PageBreak())

    story.append(Paragraph("5.4 Consideraciones de Ejecución", styles['Heading3']))
    execution_text = f"""
La generación del informe se realizó con {num_runs} corridas independientes de 480 minutos cada una. Cada ejecución usa una semilla distinta para asegurar independencia y reproducibilidad de los escenarios generados.<br/>
El análisis multi-run calcula medias muestrales, varianzas y el intervalo de confianza al 95% para la ganancia, el tiempo de espera promedio y el tiempo total promedio en el sistema.<br/>
La gráfica de convergencia muestra cómo se estabiliza la estimación de ganancia promedio a medida que aumentan las corridas. Estos resultados permiten evaluar la calidad del estimador y la consistencia del modelo.<br/>
El código fuente completo y la implementación están disponibles en GitHub: <a href="https://github.com/ChickenLittle02/Proyecto_Eventos_Discretos">https://github.com/ChickenLittle02/Proyecto_Eventos_Discretos</a>.
    """
    story.append(Paragraph(execution_text, body_style))
    story.append(PageBreak())
    
    # ========== CONCLUSIONES ==========
    story.append(Paragraph("6. CONCLUSIONES", heading_style))
    
    conclusion_text = f"""
Basado en {num_runs} simulaciones independientes del taller Happy Computing, se obtuvieron los siguientes resultados:<br/>
<br/>
<b>• Ganancia esperada:</b> ${mean_profit:.2f} por jornada de 8 horas, con intervalo de confianza al 95% 
de [${ci_low:.2f}, ${ci_high:.2f}].<br/>
<br/>
<b>• Clientes servidos:</b> En promedio {np.mean(clients_array):.1f} clientes por jornada, con variabilidad 
de {np.std(clients_array, ddof=1):.2f} clientes.<br/>
<br/>
<b>• Mix de servicios:</b> La mayoría de clientes ({100*total_by_type[0]/total_clients_all:.1f}%) 
solicita reparación en garantía (sin costo), mientras que los servicios de pago generan la mayor parte 
de los ingresos.<br/>
<br/>
<b>• Rentabilidad:</b> El servicio de "Venta de Reparados" es el más rentable (${profits_by_type[3]:.0f} total), 
seguido por reparaciones sin garantía (${profits_by_type[1]:.0f}).<br/>
<br/>
El modelo de simulación permite a la gerencia estimar ingresos y tomar decisiones sobre asignación 
de recursos (vendedores, técnicos) para maximizar ganancias en diferentes escenarios.<br/>
<br/>
El informe y el código fuente están disponibles en GitHub: <a href="https://github.com/ChickenLittle02/Proyecto_Eventos_Discretos">https://github.com/ChickenLittle02/Proyecto_Eventos_Discretos</a>.
    """
    story.append(Paragraph(conclusion_text, body_style))
    
    # Construir PDF
    doc.build(story)
    
    print(f"✓ Informe PDF generado: {output_pdf}")
    print("=" * 70)


if __name__ == '__main__':
    generate_report(num_runs=100)
