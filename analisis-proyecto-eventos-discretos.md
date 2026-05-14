# Análisis del Proyecto: Simulación basada en Eventos Discretos

> Análisis detallado de los 6 problemas planteados, con flujo de cada uno, ranking de dificultad, recomendación de lenguaje y estructura de proyecto sugerida.

---

## 📋 Índice

1. [Recomendación general (lenguaje y librerías)](#recomendación-general)
2. [Estructura común del proyecto](#estructura-común-del-proyecto)
3. [Ranking de dificultad](#ranking-de-dificultad)
4. [Problema 1 — La Cocina de Kojo](#problema-1--la-cocina-de-kojo)
5. [Problema 2 — Puerto Sobrecargado](#problema-2--puerto-sobrecargado)
6. [Problema 3 — Canal Marítimo](#problema-3--canal-marítimo)
7. [Problema 4 — Happy Computing](#problema-4--happy-computing)
8. [Problema 5 — Aeropuerto de Barajas](#problema-5--aeropuerto-de-barajas)
9. [Problema 6 — Poblado en Evolución](#problema-6--poblado-en-evolución)
10. [Generación de variables aleatorias (clave para todos)](#generación-de-variables-aleatorias)
11. [Recomendación final: ¿cuál escoger?](#recomendación-final)

---

## Recomendación general

### Lenguaje recomendado: **Python**

**Razones:**
- El enunciado exige programar **toda la generación de variables aleatorias** (no usar funciones de alto nivel "mágicas"). Python permite implementar a mano `Uniform`, `Exponential`, `Normal` (Box-Muller) y `Poisson` de forma muy limpia.
- `numpy.random` solo se usaría para `random()` uniforme [0,1) como fuente base; el resto se construye encima.
- Manejo de colas de eventos con `heapq` (priority queue) — perfecto para DES (Discrete Event Simulation).
- `matplotlib` / `pandas` para visualizar resultados y generar gráficas para el informe.
- Sintaxis clara → el informe queda mejor cuando el código se lee bien.

**Alternativas válidas:**
- **C#** o **Java**: si te sientes mejor con tipado fuerte; más verboso pero igual de viable.
- **JavaScript/TypeScript** (Node): si quieres una interfaz web con gráficas; sobrecargado para algo que es 100% backend.
- **Evitar** Pascal/C++ puro: el costo en tiempo de implementación es alto y el profesor no te exige eficiencia, te exige claridad y correctitud estadística.

### Librerías mínimas en Python

```
numpy           # solo para random uniforme y arrays numéricos
matplotlib      # gráficas para el informe
pandas          # tablas de resultados (opcional)
```

⚠️ **NO uses `simpy`** ni librerías de simulación de alto nivel: el enunciado pide que **tú** programes el modelo de eventos discretos. Usar `simpy` te quita el componente didáctico y probablemente te baje la nota.

---

## Estructura común del proyecto

Sea cual sea el problema, te recomiendo esta estructura:

```
proyecto-eventos-discretos/
├── README.md                    # Descripción + instrucciones de uso
├── requirements.txt             # numpy, matplotlib
├── informe/
│   └── informe.pdf              # Informe entregable
├── src/
│   ├── __init__.py
│   ├── random_vars.py           # Generadores de v.a. (uniforme, exp, normal, poisson)
│   ├── event.py                 # Clase Event (tiempo, tipo, datos)
│   ├── event_queue.py           # PriorityQueue basada en heapq
│   ├── simulation.py            # Loop principal del motor DES
│   ├── entities.py              # Entidades del problema (cliente, barco, avión, persona...)
│   ├── stats.py                 # Acumuladores de estadísticas
│   └── main.py                  # CLI: parámetros y runs múltiples
├── results/
│   ├── run_001.csv
│   └── plots/
└── tests/
    └── test_random_vars.py      # Validar que las distribuciones generadas son correctas
```

### El esqueleto del motor DES (común a TODOS los problemas)

```python
import heapq

class Event:
    def __init__(self, time, kind, payload=None):
        self.time = time
        self.kind = kind
        self.payload = payload
    def __lt__(self, other):
        return self.time < other.time

class Simulation:
    def __init__(self):
        self.clock = 0.0
        self.events = []     # min-heap
        self.stats = {}

    def schedule(self, delay, kind, payload=None):
        heapq.heappush(self.events, Event(self.clock + delay, kind, payload))

    def run(self, until):
        while self.events and self.clock < until:
            ev = heapq.heappop(self.events)
            if ev.time > until: break
            self.clock = ev.time
            self.handle(ev)

    def handle(self, ev):
        # despachar según ev.kind — específico al problema
        raise NotImplementedError
```

Este esqueleto se reutiliza en los 6 problemas; lo único que cambia es `handle()` y los tipos de eventos.

---

## Ranking de dificultad

| # | Problema | Dificultad | Tiempo estimado | Por qué |
|---|----------|-----------|-----------------|---------|
| 1 | **Kojo's Kitchen** | ⭐ Muy fácil | 4–6 h | M/G/2 con tasa de llegada por tramos. Estándar. |
| 4 | **Happy Computing** | ⭐⭐ Fácil | 6–8 h | Cola con prioridad y ruteo entre roles, pero acotado. |
| 5 | **Aeropuerto de Barajas** | ⭐⭐⭐ Medio | 8–12 h | Varias fases por avión, recursos paralelos, eventos encadenados. |
| 2 | **Puerto Sobrecargado** | ⭐⭐⭐⭐ Difícil | 12–18 h | Lógica del remolcador es una máquina de estados sutil. |
| 3 | **Canal Marítimo** | ⭐⭐⭐⭐ Difícil | 12–18 h | 5 diques en cadena con capacidad variable según tamaño. |
| 6 | **Poblado en Evolución** | ⭐⭐⭐⭐⭐ Muy difícil | 20–30 h | Es agent-based más que DES; muchas interdependencias. |

### TL;DR de la elección

- **Si quieres terminar rápido y bien** → Problema 1 (Kojo).
- **Si quieres una buena nota con esfuerzo razonable** → Problema 4 (Happy Computing) o 5 (Barajas).
- **Si te gustan los retos** → Problema 2 (Puerto) o 3 (Canal).
- **Si te sientes muy cómodo y quieres algo único** → Problema 6 (Poblado), pero ojo, se sale del marco DES tradicional.

---

## Problema 1 — La Cocina de Kojo

### Resumen
Puesto de comida con dos tipos de productos (sándwich/sushi), 2 empleados fijos. Comparar con escenario de 3 empleados en horas pico. Métrica: % de clientes que esperan más de 5 min.

### Datos clave
- Horario: 10:00 am — 9:00 pm (11 horas).
- Llegadas: **exponenciales por tramos** (no homogéneo simulado como homogéneo a tramos):
  - Tramo "valle": 10:00–11:30, 13:30–17:00, 19:00–21:00.
  - Tramo "pico 1": 11:30–13:30.
  - Tramo "pico 2": 17:00–19:00.
- Servicio:
  - Sándwich: `Uniform(3, 5)` minutos.
  - Sushi: `Uniform(5, 8)` minutos.
- 2 tipos de clientes (cada uno consume **solo** una cosa). Probabilidad sándwich vs sushi: el enunciado no la fija → asumir 50/50 y documentarlo en el informe.

> ⚠️ **Hueco del enunciado**: no da las λ de cada tramo ni la proporción sándwich/sushi. **Tienes que asumir valores razonables y declararlos como parámetros**. Por ejemplo: pico λ=3 min, valle λ=8 min.

### Eventos
- `LLEGADA_CLIENTE`
- `FIN_SERVICIO(empleado_id)`

### Flujo
```
1. Inicializar: clock=0 (10:00am), 2 empleados libres, cola vacía.
2. Programar primera llegada con λ del tramo actual.
3. Loop:
   - LLEGADA:
       * decidir tipo (sándwich/sushi).
       * si hay empleado libre → asignar, programar FIN_SERVICIO.
       * si no → encolar; registrar tiempo de entrada a cola.
       * programar próxima LLEGADA usando λ del tramo en t actual.
   - FIN_SERVICIO:
       * registrar espera del cliente saliente (start_servicio - llegada).
       * si cola no vacía → tomar primero, asignar, programar FIN_SERVICIO.
4. Al cerrar (21:00) seguir atendiendo a los que ya están dentro pero no aceptar nuevas.
5. Calcular: % clientes con espera > 5 min.
```

### Estructura específica
```
src/
├── kojo/
│   ├── arrival_rates.py    # función λ(t)
│   ├── employee.py
│   ├── customer.py
│   └── kojo_sim.py
```

### Comparación de escenarios
Correr la simulación `N=1000` veces para cada escenario (2 empleados vs 3 en pico) y reportar el **promedio del %** con su intervalo de confianza al 95 %. Eso impresiona al profesor.

### Por qué es el más fácil
- Una sola cola (FIFO).
- Recursos homogéneos (cualquier empleado atiende cualquier producto).
- Métrica trivial de calcular.
- Sin interacción compleja entre entidades.

---

## Problema 2 — Puerto Sobrecargado

### Resumen
Puerto con **3 muelles** y **1 remolcador único**. Tanqueros llegan, el remolcador los lleva al muelle, cargan, y el remolcador los regresa al puerto.

### Datos clave
- Llegadas tanqueros: `Exp(λ=8 h)`.
- Tipos: pequeño (0.25), mediano (0.25), grande (0.5).
- Tiempo de carga: `Normal(9,1)`, `Normal(12,2)`, `Normal(18,3)` h.
- Remolcador llevando tanquero a muelle: `Exp(λ=2 h)`.
- Remolcador llevando tanquero al puerto: `Exp(λ=1 h)`.
- Remolcador viajando solo: `Exp(λ=15 min)`.

### El remolcador: máquina de estados
Aquí está la dificultad. El remolcador puede estar en:
1. `EN_PUERTO_OCIOSO` (esperando)
2. `LLEVANDO_TANQUERO_A_MUELLE`
3. `EN_MUELLE_OCIOSO` (poco común)
4. `LLEVANDO_TANQUERO_A_PUERTO`
5. `VIAJANDO_VACIO_A_PUERTO`
6. `VIAJANDO_VACIO_A_MUELLE`

### Política de decisión del remolcador (clave)
Cuando termina una operación, decide qué hacer con esta prioridad:
- Si acaba de **dejar un tanquero en muelle**:
  - ¿Hay algún tanquero esperando salir desde algún muelle? → llévalo al puerto.
  - Si no, ¿hay muelle vacío y barco en cola en puerto? → vuelve al puerto vacío.
  - Si no, espera ahí (raro).
- Si acaba de **llegar al puerto con un tanquero**:
  - ¿Hay barco esperando + muelle vacío? → llévalo al muelle.
  - Si no, espera en puerto.

### Eventos
- `ARRIBO_TANQUERO`
- `FIN_VIAJE_TUG_A_MUELLE` (tanquero llega al muelle, empieza a cargar)
- `FIN_CARGA(muelle)`
- `FIN_VIAJE_TUG_A_PUERTO` (tanquero sale del sistema)
- `FIN_VIAJE_TUG_VACIO` (remolcador llega vacío, decide qué hacer)

### Flujo simplificado
```
ARRIBO_TANQUERO:
   sortear tamaño; añadir a cola_puerto
   si remolcador EN_PUERTO_OCIOSO y muelle libre:
       tomarlo y programar FIN_VIAJE_TUG_A_MUELLE

FIN_VIAJE_TUG_A_MUELLE:
   ocupar muelle, programar FIN_CARGA
   decidir siguiente movimiento del remolcador (ver política)

FIN_CARGA:
   marcar tanquero como "esperando salir" en muelle
   si remolcador OCIOSO y en lugar correcto:
       programar FIN_VIAJE_TUG_A_PUERTO

FIN_VIAJE_TUG_A_PUERTO:
   liberar tanquero (registrar tiempo total y espera)
   decidir siguiente acción

FIN_VIAJE_TUG_VACIO:
   reevaluar política
```

### Por qué es difícil
- El remolcador es un recurso único compartido entre muchas operaciones.
- Hay que tener cuidado con **deadlocks lógicos** (ej: tanquero esperando salir mientras remolcador va al puerto).
- La métrica "tiempo de espera en muelle" es ambigua: ¿espera para atracar? ¿espera para zarpar? → declarar ambas en el informe.
- Tiempos de carga `Normal` pueden dar negativos → truncar con `max(0, x)`.

### Estructura
```
src/harbor/
├── tugboat.py        # FSM
├── dock.py
├── tanker.py
├── policy.py         # decide_next_move(world)
└── harbor_sim.py
```

---

## Problema 3 — Canal Marítimo

### Resumen
**5 diques** en cadena (cascada). Cada dique tiene 2 ciclos (subida/bajada) con 3 fases (entrada, transporte, salida). Capacidad por dique: 2 filas × 3 barcos medianos cada una = 6 medianos equivalentes.

### Lo crucial: capacidad por tamaño
> "el tamaño de cada uno corresponde a la mitad del anterior"
> "2 filas con espacio para el equivalente a 3 barcos medianos (1 grande y dos pequeños)"

Una fila aloja, en unidades de "pequeño" (la más fina):
- Grande = 4 pequeños
- Mediano = 2 pequeños
- Pequeño = 1 pequeño
- Cada fila = 6 pequeños (porque "1 grande + 2 pequeños" = 4+2 = 6).
- Por dique = **2 filas de 6 pequeños = 12 pequeños equivalentes**.

(Esta interpretación hay que dejarla escrita en el informe — el enunciado es ambiguo.)

### Empaquetamiento (packing) — la parte sutil
Cuando un dique va a iniciar un ciclo, hay que decidir qué barcos de la cola entran. Es un **bin packing** de 2 dimensiones (2 filas independientes). Algoritmo razonable:
- First Fit secuencial sobre la cola: para cada barco, intenta meterlo en fila 1, si no cabe en fila 2; si no cabe en ninguna, **se salta** y se intenta el siguiente (lo dice el enunciado: "el siguiente en la cola toma su lugar").

### Tiempos
- Apertura compuerta inferior: `Exp(λ=4 min)`.
- Entrada de cada barco: `Exp(λ=2 min)`.
- Transporte (subida/bajada del agua): `Exp(λ=7 min)`.
- Salida: `Exp(λ=1.5 min)` por barco.
- Llegadas por tramo horario y por tamaño (tabla del PDF).

### Flujo de un dique
```
estado: IDLE | ENTRADA | TRANSPORTE | SALIDA
ciclo: SUBIDA | BAJADA  (alternan, o se rige por demanda)

ENTRADA:
   programar tiempo de apertura compuerta
   por cada barco que entre, sumar Exp(2)
   total = apertura + sum(entradas)
   programar FIN_ENTRADA → cambia a TRANSPORTE

TRANSPORTE:
   programar Exp(7) → FIN_TRANSPORTE → SALIDA

SALIDA:
   programar 1.5 * n_barcos (suma exponenciales) → FIN_SALIDA → IDLE
   barcos pasan al siguiente dique (cola del dique j+1)
```

### Pregunta importante: ¿los barcos atraviesan los 5 diques?
El enunciado no es explícito. Lo más natural: cada barco entra al canal por un extremo (dique 1) y sale por el otro (después del dique 5), atravesando los 5 secuencialmente. Hay que documentar esa interpretación.

### Por qué es difícil
- 5 diques = 5 instancias del mismo modelo + colas entre ellos.
- Los ciclos subida/bajada pueden funcionar simultáneamente en distintos diques (paralelismo).
- Bin-packing añade complejidad.
- Tiempo de arribo Normal por tramo horario × tamaño → 9 generadores distintos.

### Estructura
```
src/canal/
├── lock.py            # un dique con su FSM
├── ship.py
├── packer.py          # bin-packing por fila
├── arrival_schedule.py
└── canal_sim.py
```

---

## Problema 4 — Happy Computing

### Resumen
Taller con 3 roles (vendedor, técnico, técnico_especializado), 4 servicios con precios. Calcular ganancia esperada en una jornada con 2V + 3T + 1TE.

### Flujo del cliente
```
LLEGADA → atendido por VENDEDOR (siempre, cualquier servicio)
   ├─ servicio 1 (garantía, $0)        → luego TÉCNICO o TE → fin
   ├─ servicio 2 (reparación, $350)    → luego TÉCNICO o TE → fin
   ├─ servicio 3 (cambio equipo, $500) → luego TÉCNICO ESPECIALIZADO → fin
   └─ servicio 4 (venta, $750)         → fin (solo vendedor)
```

### Regla de prioridad clave
> "Un técnico especializado solo realizará Reparaciones si no hay ningún cliente que desee un cambio de equipo en la cola."

Es decir, el TE **prefiere** servicios tipo 3. Solo si no hay clientes esperando cambio, atiende reparaciones.

### Datos
- Llegadas: el enunciado dice "poisson con λ=20 min". **Cuidado**: Poisson es discreta para conteos; el intervalo entre llegadas en un proceso de Poisson es exponencial. Implementar como **`Exp(λ=20 min)`** y documentarlo.
- Probabilidades de servicio: 0.45 / 0.25 / 0.10 / 0.20.
- Vendedor: `Normal(5, 2)` min.
- Técnico (rep cualquiera): `Exp(λ=20 min)`.
- Técnico especializado (cambio): `Exp(λ=15 min)`.
- TE en reparación: el enunciado no lo dice → asumir mismo tiempo que técnico (`Exp(20)`).

### Eventos
- `LLEGADA`
- `FIN_VENDEDOR(cliente)`
- `FIN_TECNICO(cliente)`
- `FIN_TECESP(cliente)`

### Lo único delicado
- Tres colas (vendedor / técnico+TE / TE solo para cambios).
- Cuando un TE termina, debe revisar **primero** la cola de cambios; si está vacía, mira la cola de reparaciones.
- Cuando un técnico normal termina, solo mira reparaciones.

### Métrica
Sumar `precio` de cada cliente atendido **completamente** durante la jornada (8h o 12h, hay que asumir).

### Por qué es fácil-medio
- Múltiples recursos heterogéneos pero con reglas claras.
- Sin geografía/fases.
- Buena oportunidad de hacer experimentación: probar 1V/4T/1TE, 2V/2T/2TE, etc., y graficar ganancia vs configuración.

### Estructura
```
src/repair/
├── employee.py
├── service.py
├── customer.py
├── policy.py        # asignación de cliente a empleado
└── repair_sim.py
```

---

## Problema 5 — Aeropuerto de Barajas

### Resumen
5 pistas. Avión llega, aterriza, recarga combustible, carga/descarga, posiblemente se rompe y repara, despega. Métrica: tiempo total que cada pista está vacía durante una semana.

### Datos
- Llegadas: `Exp(λ=20 min)`.
- Aterrizaje/despegue: `Normal(10, 5)` min.
- Carga/descarga: `Exp(λ=30 min)`.
- Recarga combustible: `Exp(λ=30 min)`, **simultánea con carga/descarga**, empieza al aterrizar.
- Probabilidad de carga = `Uniform(0,1) > umbral` (asumir 0.5) — **otro hueco**.
- Probabilidad rotura = 0.1, detectada antes de despegar.
- Reparación: `Exp(λ=15 min)`.

### Operaciones simultáneas vs secuenciales
Un avión, mientras está en pista:
- Aterriza (secuencial, primero).
- En paralelo: recarga combustible **y** carga/descarga (si toca cargar/descargar).
- El avión está listo cuando **ambas** terminan (es decir, max(t_combustible, t_carga)).
- Antes de despegar: chequeo → quizá rotura → reparación.
- Despega.

### Eventos
- `ARRIBO_AVION`
- `FIN_ATERRIZAJE(pista, avion)` → arranca combustible y carga
- `FIN_COMBUSTIBLE(pista)`
- `FIN_CARGA(pista)`
- `FIN_REPARACION(pista)`  (solo si hubo rotura)
- `FIN_DESPEGUE(pista)` → libera pista

### Pista vacía
"Una pista está ocupada cuando hay un avión aterrizando, despegando, cargando, descargando o el abordaje".
→ pista ocupada = desde `inicio_aterrizaje` hasta `fin_despegue` (cubre todo el ciclo).
→ pista vacía = tiempo total simulado (1 semana = 10080 min) menos suma de ciclos por pista.

### Por qué es medio
- Hay **paralelismo intra-avión** (combustible || carga). Necesitas una variable "fases pendientes" en cada avión y solo despegar cuando todas estén en 0.
- 5 recursos idénticos con cola única.
- Una semana de simulación → asegúrate de que el algoritmo sea eficiente (lista de eventos puede crecer; con heap está bien).

### Estructura
```
src/airport/
├── runway.py
├── plane.py
├── arrival.py
└── airport_sim.py
```

---

## Problema 6 — Poblado en Evolución

### Resumen
Simulación de población durante 100 años con dinámica de muertes, parejas, embarazos, partos múltiples. Inicial: M mujeres + H hombres con edad `Uniform(0, 100)`.

### Por qué es el más difícil (y atípico)
**Esto NO es DES en el sentido clásico** — es una **simulación basada en agentes** con paso de tiempo (típicamente discretizada por meses o años). Cada persona es un agente con estado (edad, sexo, soltero/en pareja, hijos teñidos, hijos deseados, etc.).

Hay dos enfoques:

**A) Agent-based con paso de tiempo (recomendado para este problema):**
```
para cada año (o mes):
   para cada persona:
       envejecer
       chequear muerte → eliminar si fallece
       chequear ruptura/separación
       si soltera y libre del periodo de luto → buscar pareja
       si mujer en pareja → chequear embarazo → si sí, programar parto en 9 meses
   procesar nacimientos
   recolectar estadísticas
```

**B) Híbrido DES**: cada persona tiene eventos programados (muerte futura, fin de luto, parto). Se vuelve un infierno de actualizaciones porque la probabilidad de morir cambia con la edad.

### Datos a respetar (todos en el PDF)
- Probabilidad muerte por (edad, sexo).
- Probabilidad embarazo por edad de la mujer.
- Número de hijos deseados por persona (la pareja respeta el mínimo entre los dos).
- Probabilidad de querer pareja por edad.
- Probabilidad de "match" según diferencia de edad.
- Probabilidad ruptura = 0.2 (¿anual? — asumir anual y declararlo).
- Periodo de soledad post-ruptura: exponencial con λ por edad.
- Embarazo múltiple (1 a 5 bebés con probabilidades dadas).
- Sexo del bebé: 50/50.

### Ojo a las probabilidades del enunciado
> Número de hijos deseados:
> 1: 0.6, 2: 0.75, 3: 0.35, 4: 0.2, 5: 0.1, más de 5: 0.05
> 
> Eso suma 2.45, ¡no 1! → **interpretar como CDF acumulada**: P(deseo ≥ 1) = 0.6, P(≥2) = 0.75... Esto tampoco encaja porque no es monótona. Lo más probable es que sean **probabilidades sin normalizar** y haya que **normalizar dividiendo por la suma**.
> 
> En el informe: declarar la decisión y explicarla.

Igual pasa con "Número de bebés" (suma 1.02 si tomas 0.7 + 0.18 + 0.08 + 0.04 + 0.02): el "0.7 meses" está mal escrito, debería ser solo 0.7. → asumir y normalizar.

### Métrica de salida
Series temporales año a año: total de habitantes, distribución por edad, ratio H/M, número de parejas, tasa de natalidad, tasa de mortalidad. Genera buenas gráficas para el informe.

### Estructura
```
src/population/
├── person.py
├── couple.py
├── world.py        # contiene a todas las personas
├── distributions.py # tablas del PDF
└── pop_sim.py
```

### Recomendación honesta
**No es el mejor problema para alguien que recién aprende DES**: el modelo de eventos puro encaja mal. Si lo eliges, el riesgo de entregar algo medio funcional es alto. Pero si dominas Python y POO, puede quedar muy lucido (¡con gráficas de pirámides poblacionales!).

---

## Generación de variables aleatorias

> El enunciado pide explícitamente programar **a mano** las distribuciones. Esta es la implementación mínima que necesitas para todos los problemas:

```python
import math
import random  # solo random() uniforme [0,1)

def uniform(a, b):
    return a + (b - a) * random.random()

def exponential(lam):
    # método de inversa: -ln(U)/λ. Si λ está en "media" (ej. λ=8h media):
    # entonces tasa = 1/8 y la fórmula es -ln(U) * media.
    # ⚠️ El PDF mezcla "λ = 8 horas" como MEDIA, no como tasa.
    return -math.log(1 - random.random()) * lam   # interpretando λ como media

def normal(mu, sigma):
    # Box-Muller
    u1 = 1 - random.random()
    u2 = 1 - random.random()
    z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mu + sigma * z

def poisson(lam):
    # algoritmo de Knuth (cuenta hasta superar e^-λ)
    L = math.exp(-lam)
    k, p = 0, 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def discrete(probabilities):
    # probabilidades = lista de pares [(valor, p)] que sumen 1
    u = random.random()
    cum = 0.0
    for v, p in probabilities:
        cum += p
        if u <= cum:
            return v
    return probabilities[-1][0]
```

⚠️ **Cuidado con la convención de λ**: el PDF usa "λ = 8 horas" para una **exponencial con media 8 h**. En matemáticas, λ suele ser la **tasa** = 1/media. Tienes dos opciones; declara cuál usas en el informe y sé consistente.

⚠️ La normal puede dar negativos. En tiempos de servicio, **truncar** (`max(0, x)`) o **rechazar y regenerar**. Documentar la elección.

---

## Recomendación final

### Si me preguntas a mí: **Problema 1 (Kojo) o Problema 4 (Happy Computing)**.

**Por qué Kojo**:
- Es el más rápido de hacer.
- La métrica es clara y tiene una comparación interesante (escenario A vs B), lo cual da material rico para el informe (gráficas, intervalos de confianza, conclusiones).
- Bajo riesgo de quedar atascado.

**Por qué Happy Computing**:
- Más interesante intelectualmente que Kojo (ruteo entre roles).
- Permite experimentar variando configuraciones de empleados → buenas conclusiones.
- Sigue siendo abordable en un fin de semana.

### Lo que más le gusta a un profesor de simulación

1. **Que la generación de variables aleatorias esté hecha a mano** y validada (tests de chi-cuadrado o KS aunque sea visuales).
2. **Múltiples corridas** (mín. 100, idealmente 1000) y reporte de **media + intervalo de confianza**, no una sola corrida.
3. **Gráficas**: histograma de tiempos de espera, evolución del sistema en una corrida típica, comparación entre escenarios.
4. **Discusión de las suposiciones**: cada vez que el enunciado tenga un hueco, decláralo en el informe ("Asumimos λ_pico=3min porque el enunciado no lo especifica").
5. **Validación**: si puedes calcular analíticamente algo (ej. utilización de los empleados en Kojo en estado estacionario para comparar), hazlo.

### Checklist final antes de entregar

- [ ] Repositorio público en GitHub con README claro.
- [ ] Instrucciones de "cómo correr" en el README.
- [ ] `requirements.txt`.
- [ ] Generadores de v.a. propios (sin `numpy.random.exponential` etc.).
- [ ] Múltiples corridas con semilla configurable.
- [ ] Gráficas y CSV de resultados.
- [ ] Informe PDF con: datos del estudiante, problema asignado, ideas, modelo DES (lista de eventos + diagrama), suposiciones declaradas, resultados con IC, conclusiones, link al repo.

---

## Comparativa rápida de problemas

| Aspecto | Kojo | Puerto | Canal | HappyC | Barajas | Poblado |
|---------|------|--------|-------|--------|---------|---------|
| Eventos distintos | 2 | 5 | 4 | 4 | 5 | depende |
| Recursos | 2-3 emp | 3 muelles + 1 tug | 5 diques | 6 emp | 5 pistas | N/A |
| Lógica de cola | trivial | compleja (tug FSM) | bin-packing | con prioridad | trivial | N/A |
| Paralelismo intra-entidad | no | no | no | no | sí (combust+carga) | no |
| Ambigüedad enunciado | media | baja | alta | baja | media | alta |
| Riesgo de no terminar | bajo | medio | alto | bajo | medio | alto |
| Material para informe | bueno | excelente | excelente | bueno | bueno | excelente |
