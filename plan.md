Tomando en cuenta **solo los primeros 4 temas del libro** (modelación, generación de variables aleatorias, eventos discretos y análisis estadístico), el proyecto que te recomiendo **NO escoger** es:

* **Canal Marítimo (#3)** → demasiados estados + reglas de capacidad + múltiples diques.
* **Poblado en Evolución (#6)** → demasiado complejo, muchas reglas probabilísticas.
* **Puerto Sobrecargado (#2)** → lógica del remolcador bastante enredada.
* **Aeropuerto (#5)** → muchos eventos simultáneos (aterrizaje, combustible, reparación, carga, despegue).

Esos te pueden consumir más de 2 días fácilmente.

---

## El mejor balance (ni muy fácil ni muy difícil): **Proyecto #4 – Happy Computing**



¿Por qué te recomiendo este?

### Lo que usa del libro:

✅ **Capítulo 2:** generar variables aleatorias

* Exponencial → tiempos entre llegadas
* Exponencial → tiempo de reparación
* Exponencial → cambio de equipo
* Normal → tiempo de atención del vendedor
* Probabilidades discretas → tipo de servicio

✅ **Capítulo 3:** eventos discretos
Eventos clarísimos:

* llegada cliente
* fin atención vendedor
* fin reparación técnico
* fin cambio técnico especializado

✅ **Capítulo 4:** análisis estadístico
Puedes correr la simulación varias veces y calcular:

* ganancia promedio
* varianza
* desviación estándar

---

# ¿Por qué NO es demasiado fácil?

Porque sí tienes que manejar:

* múltiples servidores
* colas
* prioridad del técnico especializado:

  > solo hace reparaciones si no hay clientes esperando cambio de equipo

Eso le da suficiente complejidad para que el profesor vea trabajo real.

---

# ¿Por qué es más fácil que otros?

A diferencia del puerto o aeropuerto:

* no hay demasiados eventos raros
* no hay múltiples fases por cliente
* no hay restricciones físicas complejas
* la lógica es bastante natural

Básicamente es una **cola multiserver con prioridades**.

---

# Complejidad real estimada

Si programas rápido en Python/Java/C++:

### Simulación básica:

4–6 horas

### Debug:

3–5 horas

### Estadísticas:

2 horas

### Informe:

3–4 horas

Total:
**12–17 horas reales**

En 2 días sí sale.

---

# Cómo modelarlo

## Eventos

### 1. Llegada de cliente

Generar próxima llegada:

[
T=-20\ln(U)
]

(Exponencial λ=20 min)

T=-20\ln(U)

---

## Tipo de servicio

Usas probabilidades:

* reparación garantía → 0.45
* reparación fuera garantía → 0.25
* cambio equipo → 0.10
* venta reparados → 0.20

---

## Atención vendedor

Distribución normal:

[
N(5,2)
]

---

## Técnico normal

Reparaciones:

[
T=-20\ln(U)
]

T=-20\ln(U)

---

## Técnico especializado

Cambio de equipo:

[
T=-15\ln(U)
]

T=-15\ln(U)

---

# Recursos

* 2 vendedores
* 3 técnicos
* 1 técnico especializado

---

# Variables de estado

```text
t → tiempo actual
cola_vendedores
cola_tecnicos
cola_especializados
ganancia_total
clientes_atendidos
```

---

# Métrica final

El problema pide:

> ganancia en una jornada laboral

Entonces calculas:

[
ganancia=\sum servicios cobrados
]

* tipo 1 → $0
* tipo 2 → $350
* tipo 3 → $500
* tipo 4 → $750

---

# Plan para terminarlo en 2 días

---

## Día 1 (8–10 horas)

### Hora 1–2

Leer bien el problema y definir:

* eventos
* variables
* colores
* flujo

Haz un diagrama rápido.

---

### Hora 3–5

Implementar generadores aleatorios:

* exponencial
* normal
* tipo servicio

---

### Hora 6–8

Implementar:

* llegada
* cola vendedores
* cola técnicos

---

### Hora 9–10

Implementar técnico especializado + prioridades

---

## Resultado esperado día 1:

Simulación funcionando aunque tenga bugs pequeños.

---

# Día 2 (8–10 horas)

### Hora 1–3

Debug completo

Revisa:

* clientes perdidos
* tiempos negativos
* colas infinitas
* doble atención

---

### Hora 4–5

Correr 30 simulaciones

Tal como dice capítulo 4:

[
\bar X=\frac{\sum X_i}{n}
]

\bar{X}=\frac{\sum X_i}{n}

y varianza muestral:

[
S^2=\frac{\sum (X_i-\bar X)^2}{n-1}
]

genui{"math_block_widget_always_prefetch_v2":{"content":"S^2=\frac{\sum (X_i-\bar{X})^2}{n-1}"}}

---

### Hora 6–8

Escribir informe PDF:

* descripción
* modelo
* eventos
* resultados

---

### Hora 9–10

Subir a GitHub y revisar entrega

---

# Si quieres algo aún más fácil

El más fácil sería **Kojo’s Kitchen (#1)** porque solo comparas:

* 2 empleados
* vs
* 3 empleados en horas pico

Pero siento que puede verse demasiado básico.

---

# Mi ranking honesto

### Mejor balance:

🥇 Happy Computing (#4)

### Más fácil:

🥈 Kojo’s Kitchen (#1)

### Más difícil:

🥉 Puerto / Canal / Aeropuerto / Poblado

---

Si solo tienes **48 horas y quieres minimizar riesgo**, escoge **Happy Computing**.
Si tienes menos de 24 horas, entonces vete con **Kojo’s Kitchen**.
---

# IMPLEMENTACIÓN ACTUAL - Happy Computing

## ✅ YA IMPLEMENTADO

### Fase 1: Infraestructura Base
- ✅ Estructura de directorios (src/, results/, tests/, informe/)
- ✅ Generadores de variables aleatorias:
  - `uniform(a, b)` → distribución uniforme
  - `exponential(rate)` → exponencial con parámetro λ
  - `normal_box_muller(mu, sigma)` → normal con Box-Muller
  - `discrete(probs)` → variable discreta por probabilidades

### Fase 2: Motor de Simulación
- ✅ Clase `Event` → representa eventos con tiempo, tipo y payload
- ✅ Clase `EventQueue` → cola de prioridad con heapq
- ✅ Clase `Simulation` (base) → reloj, scheduling, loop principal

### Fase 3: Modelado del Problema
- ✅ Entidades: `Client`, `Seller`, `Technician`, `ServiceType`
- ✅ Lógica principal en `HappyComputingSimulation`:
  - Llegadas exponenciales (λ=1/20)
  - Asignación a vendedores (2 vendedores, cola FIFO)
  - Atención vendedor Normal(5,2)
  - Ruteo a técnico normal o especializado según tipo de servicio
  - Reparaciones exponenciales (λ=1/20 o λ=1/15)
  - Cálculo de ganancias por tipo de servicio

### Fase 4: Ejecución Básica
- ✅ Script `main.py` con múltiples runs (100 simulaciones)
- ✅ Estadísticas básicas: ganancia promedio ± desviación estándar

**Estado**: La simulación **funciona y produce resultados coherentes**
- Ganancia promedio: ~$5391 por jornada (8 horas)
- Clientes atendidos: ~21 por jornada

---

## ❌ FALTA POR IMPLEMENTAR

### OPCIÓN A: Mínimo para aprobación (4-5 horas)

1. **Tests unitarios para generadores de v.a.** (1-2 horas)
   - Verificar que exponential(20) tiene media ≈ 20
   - Verificar que normal(5,2) produce N(5,2)
   - Prueba Kolmogorov-Smirnov

2. **Debug y validación** (1-2 horas)
   - Verificar que: clientes_llegados == clientes_atendidos
   - Revisar colas al final (¿hay clientes atrapados?)
   - Validar tiempos (sin negativos)

3. **Estadísticas mejoradas** (30 min)
   - Agregar: min, max, mediana, percentiles, intervalo confianza 95%

4. **Una visualización** (1 hora)
   - Histograma de ganancias con media y desviación

5. **Informe básico** (1-2 horas)
   - Descripción del modelo
   - Diagrama de flujo
   - Resultados + gráfica

### OPCIÓN B: Completo (8-12 horas - después de A)

6. **Exportar datos a CSV** (1 hora)
   - Por cliente: arrival_time, service_type, wait_time, departure_time, profit
   - Resumen por run: run_number, total_profit, clients_served, avg_wait_time

7. **Análisis de colas y recursos** (1-2 horas)
   - Longitud promedio de cada cola
   - Utilización de recursos (% de tiempo ocupado)
   - Tiempo máximo en cola

8. **Visualizaciones completas** (2-3 horas)
   - Histograma de ganancias
   - Boxplot de ganancias
   - Evolución de colas a lo largo del tiempo
   - Tiempos de espera vs. tiempo de llegada

9. **Validación de distribuciones** (1-2 horas)
   - Histogramas vs. teóricas
   - Q-Q plots
   - Verificar que las v.a. generadas coinciden con lo esperado

10. **Análisis avanzado** (1-2 horas)
    - Correlación entre tipo de servicio y tiempo de espera
    - Análisis de sensibilidad (qué pasa con 1, 2, 3, 4 técnicos)

11. **Informe completo en PDF** (2-3 horas)
    - Con todas las gráficas
    - Análisis estadístico
    - Conclusiones

---

## 📋 ORDEN RECOMENDADO

### Semana 1: OPCIÓN A (4-5 horas)

```
Lunes 15 mayo
├─ 13:00-14:30: Tests unitarios para generadores
├─ 14:30-16:00: Debug y validación de lógica
└─ 16:00-16:30: Estadísticas mejoradas

Martes 16 mayo
├─ 09:00-10:00: Primera visualización (histograma)
└─ 10:00-12:00: Informe básico PDF
```

**Entrega**: 12 mayo, con:
- Código validado
- 1 gráfica
- Informe básico

---

### Semana 2: OPCIÓN B (8+ horas extra)

```
Miércoles 17 mayo
├─ 09:00-10:00: Exportar datos a CSV
├─ 10:00-11:00: Análisis de colas/recursos
└─ 11:00-14:00: Visualizaciones completas (boxplot, evolución de colas)

Jueves 18 mayo
├─ 09:00-11:00: Validación de distribuciones
├─ 11:00-12:00: Análisis avanzado (sensibilidad)
└─ 13:00-16:00: Informe completo con todos los análisis
```

**Entrega final**: con análisis exhaustivo

---

## 🎯 CHECKLIST DE TAREAS

### OPCIÓN A
- [ ] 1. Crear tests/test_random_vars.py (pruebas unitarias)
- [ ] 2. Implementar debug y validación de clientes
- [ ] 3. Expandir stats.py con estadísticas completas
- [ ] 4. Crear plots.py con funciones de visualización
- [ ] 5. Generar histograma de ganancias
- [ ] 6. Escribir informe básico en PDF

### OPCIÓN B (después de A)
- [ ] 7. Crear función para exportar a CSV
- [ ] 8. Implementar análisis de colas y recursos
- [ ] 9. Agregar visualizaciones adicionales (boxplot, evolución)
- [ ] 10. Crear plots de validación de distribuciones
- [ ] 11. Análisis de sensibilidad
- [ ] 12. Informe completo con todos los análisis