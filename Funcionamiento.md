Te voy a explicar cada componente del proyecto, cómo funciona y el objetivo. Comencemos por entender la estructura general.    

Read [](file:///home/nebur02/Documents/3er%20Ano/2do%20SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src/random_vars.py)

Read [](file:///home/nebur02/Documents/3er%20Ano/2do%20SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src/event.py)

Read [](file:///home/nebur02/Documents/3er%20Ano/2do%20SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src/event_queue.py)

Read [](file:///home/nebur02/Documents/3er%20Ano/2do%20SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src/simulation.py)

Read [](file:///home/nebur02/Documents/3er%20Ano/2do%20SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src/happy_computing.py#1-1), lines 1 to 50

Read [](file:///home/nebur02/Documents/3er%20Ano/2do%20SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/src/entities.py)

Perfecto, voy a explicarte cada componente del proyecto paso a paso:

---

## **1️⃣ GENERADORES DE VARIABLES ALEATORIAS** (random_vars.py)

Este es el **corazón matemático** del proyecto. Aquí implementamos los generadores que requiere el problema:

```python
class RandomVars:
    def uniform(self, a=0, b=1):
        """Genera número aleatorio entre a y b"""
        return self.rng.uniform(a, b)
```
✅ **Uniforme**: Base de todo. Genera números entre 0 y 1. Las otras se construyen sobre esta.

```python
    def exponential(self, rate):
        """Genera variable exponencial con media = 1/rate"""
        u = self.uniform()
        return -math.log(u) / rate
```
✅ **Exponencial**: Formula matemática: $ T = -\ln(U) / \lambda $  
- En el problema se usa para:
  - Tiempo entre **llegadas de clientes** (media 20 min)
  - Tiempo de **reparación normal** (media 20 min)
  - Tiempo de **cambio especializado** (media 15 min)

```python
    def normal_box_muller(self, mu=0, sigma=1):
        """Genera variable normal N(μ, σ) con Box-Muller"""
        u1 = self.uniform()
        u2 = self.uniform()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mu + sigma * z0
```
✅ **Normal (Box-Muller)**: Para el tiempo que tardan los **vendedores atendiendo** N(5, 2).

```python
    def discrete(self, probs):
        """Genera variable discreta dada una lista de probabilidades"""
        u = self.uniform()
        cumulative = 0
        for i, p in enumerate(probs):
            cumulative += p
            if u < cumulative:
                return i
```
✅ **Discreta**: Elige el **tipo de servicio** según probabilidades:
- 45% → reparación garantía ($0)
- 25% → reparación sin garantía ($350)
- 10% → cambio equipo ($500)
- 20% → venta de reparados ($750)

---

## **2️⃣ SISTEMA DE EVENTOS** (event.py, event_queue.py)

### `Event` - Representa un evento

```python
class Event:
    def __init__(self, time, kind, payload=None):
        self.time = time      # Cuándo ocurre
        self.kind = kind      # Qué tipo: 'ARRIVAL', 'SELLER_END', etc.
        self.payload = payload # Datos adicionales: ID del vendedor, etc.

    def __lt__(self, other):
        return self.time < other.time  # Importante: ordena por tiempo
```

**Objetivo**: Cada evento es "algo que sucede en un momento en el tiempo".
- Ejemplo: `Event(time=23.5, kind='ARRIVAL', payload=None)` → cliente llega a las 23.5 minutos

### `EventQueue` - Cola de prioridad

```python
class EventQueue:
    def __init__(self):
        self.queue = []  # Heap binario (Python's heapq)

    def push(self, event):
        heapq.heappush(self.queue, event)  # Inserta manteniendo orden

    def pop(self):
        return heapq.heappop(self.queue)   # Saca el evento con menor tiempo
```

**Objetivo**: Mantener ordenados los eventos por hora. Como tenemos `__lt__`, Python los ordena automáticamente por `time`.

**Visualización del funcionamiento**:
```
Estado inicial:        Después de push(E3):    Después de push(E1):
[]                     [E3(t=5)]              [E1(t=2), E3(t=5)]

Pop devuelve E1(t=2):
[E3(t=5)]
```

---

## **3️⃣ BASE DE SIMULACIÓN** (simulation.py)

```python
class Simulation:
    def __init__(self):
        self.clock = 0.0              # Reloj de la simulación
        self.event_queue = EventQueue() # Cola de eventos
```

✅ **El reloj** (`clock`): Comienza en 0 y avanza cada vez que procesamos un evento.

```python
    def schedule(self, delay, kind, payload=None):
        """Programa un evento para el futuro"""
        self.event_queue.push(Event(self.clock + delay, kind, payload))
```

✅ **Scheduling**: Si estamos en time=10 y queremos programar algo en 5 minutos más, hacemos:
```python
self.schedule(5, 'SELLER_END', seller_id=0)
# Se crea: Event(time=15, kind='SELLER_END', payload=0)
```

```python
    def run(self, until):
        """Motor principal: procesa eventos hasta tiempo 'until'"""
        while not self.event_queue.is_empty():
            event = self.event_queue.pop()  # Saca evento más próximo
            if event.time > until:
                break
            self.clock = event.time  # Avanza el reloj
            self.handle_event(event)  # Lo procesa
```

**Flujo de la simulación** (lo que hace cada iteración):
1. Saca el evento con menor tiempo de la cola
2. Si sobrepasa `until`, para
3. Avanza el reloj a ese tiempo
4. Procesa el evento

---

## **4️⃣ ENTIDADES DEL PROBLEMA** (entities.py)

```python
class ServiceType(Enum):
    REPAIR_WARRANTY = 0      # $0 (no gana dinero)
    REPAIR_NO_WARRANTY = 1   # $350
    EQUIPMENT_CHANGE = 2     # $500
    SALE_REPAIRED = 3        # $750
```

Las 4 formas en que puede llegar un cliente.

```python
class Client:
    def __init__(self, arrival_time, service_type):
        self.arrival_time = arrival_time      # Cuándo llegó
        self.service_type = service_type      # Qué necesita
        self.service_start_time = None        # Cuándo comenzó atención
        self.departure_time = None            # Cuándo se fue
```

Seguimiento completo de cada cliente durante la simulación.

```python
class Seller:
    def __init__(self, id):
        self.id = id                 # Vendedor 0 o 1
        self.busy = False            # ¿Está atendiendo?
        self.current_client = None   # A quién atiende
```

```python
class Technician:
    def __init__(self, id, specialized=False):
        self.id = id                 # Técnico 0, 1, o 2 (o especializado)
        self.specialized = specialized
        self.busy = False
        self.current_client = None
```

---

## **5️⃣ SIMULACIÓN ESPECÍFICA: HAPPY COMPUTING** (happy_computing.py)

Este es donde ocurre **toda la lógica del problema**.

```python
class HappyComputingSimulation(Simulation):
    def __init__(self, seed=None):
        super().__init__()  # Hereda de Simulation
        self.random = RandomVars(seed)  # Generador de aleatorios
```

### Recursos y Colas

```python
self.sellers = [Seller(i) for i in range(2)]           # 2 vendedores
self.technicians = [Technician(i) for i in range(3)]   # 3 técnicos
self.specialized_technician = Technician(0, specialized=True)

self.seller_queue = deque()           # Cola de clientes esperando vendedor
self.technician_queue = deque()       # Cola para técnicos normales
self.specialized_queue = deque()      # Cola para cambios de equipo
```

### Parámetros del Problema

```python
self.arrival_rate = 1/20              # Clientes llegan cada 20 min (media)
self.repair_rate = 1/20               # Reparación toma 20 min (media)
self.change_rate = 1/15               # Cambio toma 15 min (media)
self.service_mu = 5
self.service_sigma = 2                # Vendedor: N(5,2) minutos
self.service_probs = [0.45, 0.25, 0.10, 0.20]
self.profits = [0, 350, 500, 750]     # Ganancias por tipo de servicio
```

---

## **6️⃣ FLUJO DE EVENTOS**

```python
def handle_arrival(self):
    # 1. Crear cliente con tipo de servicio aleatorio
    service_type = ServiceType(self.random.discrete(self.service_probs))
    client = Client(self.clock, service_type)

    # 2. Rutear según tipo
    if service_type in [REPAIR_WARRANTY, REPAIR_NO_WARRANTY, SALE_REPAIRED]:
        self.assign_to_seller(client)
    elif service_type == EQUIPMENT_CHANGE:
        self.assign_to_specialized(client)

    # 3. Programar próxima llegada
    self.schedule(self.random.exponential(self.arrival_rate), 'ARRIVAL')
```

**Visualización del flujo de un cliente**:

```
┌─────────────────────────────────────────────────────────┐
│  Cliente llega (ARRIVAL event)                          │
└────────────────────┬────────────────────────────────────┘
                     ↓
         ¿Qué tipo de servicio?
         ├─ 45% REPAIR_WARRANTY (reparación garantía)
         ├─ 25% REPAIR_NO_WARRANTY (reparación paga)
         ├─ 10% EQUIPMENT_CHANGE (cambio equipo)
         └─ 20% SALE_REPAIRED (equipo reparado)
                     ↓
    ┌───────────────────────────────────┐
    │  Si es reparación o venta:        │
    │  Cola de VENDEDOR                 │
    └────────┬────────────────────────┘
             ↓
    ┌────────────────────────┐
    │ Vendedor (N(5,2) min)  │ → Si es reparación, va a técnico
    │ (SELLER_END event)     │   Si es venta, FIN
    └────────┬────────────────┘
             ↓
         Técnico (20 min)
         (TECHNICIAN_END) → FIN
    
    ┌───────────────────────────────────┐
    │  Si es EQUIPMENT_CHANGE:          │
    │  Cola de TÉCNICO ESPECIALIZADO    │
    └────────┬────────────────────────┘
             ↓
    ┌─────────────────────────────┐
    │ Especializado (15 min)      │
    │ (SPECIALIZED_END event)     │ → FIN
    └─────────────────────────────┘
```

---

## **7️⃣ ASIGNACIÓN DE RECURSOS**

```python
def assign_to_seller(self, client):
    # Busca un vendedor libre
    free_seller = next((s for s in self.sellers if not s.busy), None)
    if free_seller:
        # ¡Hay vendedor libre! Lo asigna inmediatamente
        self.start_seller_service(free_seller, client)
    else:
        # Todos ocupados → Encola al cliente
        self.seller_queue.append(client)

def start_seller_service(self, seller, client):
    seller.busy = True
    seller.current_client = client
    client.service_start_time = self.clock
    
    # Genera tiempo de atención (Normal)
    service_time = self.random.normal_box_muller(self.service_mu, self.service_sigma)
    
    # Programa fin de servicio
    self.schedule(service_time, 'SELLER_END', seller.id)
```

---

## **8️⃣ FIN DE SERVICIO Y DESENCUAMIENTO**

```python
def handle_seller_end(self, seller_id):
    seller = self.sellers[seller_id]
    client = seller.current_client
    
    # Registra ganancia
    self.stats.add_profit(self.profits[client.service_type.value])
    
    # Libera vendedor
    seller.busy = False
    seller.current_client = None

    # Si necesita técnico (reparación), lo envía
    if client.service_type in [REPAIR_WARRANTY, REPAIR_NO_WARRANTY]:
        self.assign_to_technician(client)
    # Si era venta, simplemente termina

    # ¡IMPORTANTE! Sirve al siguiente en la cola
    if self.seller_queue:
        next_client = self.seller_queue.popleft()
        self.start_seller_service(seller, next_client)
```

---

## **9️⃣ ESTADÍSTICAS** (`stats.py`)

```python
class Stats:
    def __init__(self):
        self.total_profit = 0
        self.clients_served = 0

    def add_profit(self, amount):
        self.total_profit += amount
```

Simplemente acumula la ganancia total y cuenta clientes.

---

## **🔟 SCRIPT PRINCIPAL** (main.py)

```python
def main():
    num_runs = 100
    profits = []

    for i in range(num_runs):
        sim = HappyComputingSimulation(seed=i)
        stats = sim.run_simulation(480)  # 8 horas
        profits.append(stats.total_profit)

    avg_profit = np.mean(profits)
    std_profit = np.std(profits)
    print(f"Ganancia promedio: ${avg_profit:.2f} ± ${std_profit:.2f}")
```

Corre la simulación **100 veces independientes** para obtener estadísticas robustas.

---

## **📊 RESUMEN DEL FLUJO COMPLETO**

```
INICIO
  ↓
┌─────────────────────────────────┐
│ Crea simulación                 │
│ - 2 vendedores (libres)         │
│ - 3 técnicos (libres)           │
│ - 1 especializado (libre)       │
│ - Colas vacías                  │
└────────────┬────────────────────┘
             ↓
    Programa primer ARRIVAL
             ↓
    ┌───────────────────────────────────┐
    │ Loop: mientras hay eventos        │
    │ y clock < 480 min                 │
    └────────────┬────────────────────┘
                 ↓
        Saca próximo evento
                 ↓
        Procesa (ARRIVAL/END)
                 ↓
        ¿Más eventos?
        ├─ Sí → vuelve al loop
        └─ No → FIN
             ↓
        Retorna ganancias totales
             ↓
    Repite 100 veces
             ↓
    Calcula promedio y desviación
```

---

## **💡 CONCEPTO CLAVE: EL RELOJ DE EVENTOS**

A diferencia de una simulación "tiempo real" que avanzaría segundo a segundo, la **simulación de eventos discretos** salta directamente a los momentos donde sucede algo:

```
Tiempo real:  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
              0 1 2 3 4 5 6 7 8 9 10...

Eventos DES:  ○       ○     ○        ○
              0.3    2.5    5.7      8.2
              (Los únicos momentos que importan)
```

¡Es mucho más eficiente! No gastamos tiempo simulando cuando nada ocurre.

---

¿Hay algún componente específico que quieras que profundice más? 🤔