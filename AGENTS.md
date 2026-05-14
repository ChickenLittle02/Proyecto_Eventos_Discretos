# AGENTS.md - Happy Computing Discrete Event Simulation

## Project Overview
This is a discrete event simulation (DES) for "Happy Computing", a computer repair shop. Clients arrive randomly, choose service types (warranty repair, no-warranty repair, equipment change, sale), and are routed through sellers and technicians. The simulation runs 100 times over 8-hour days to collect profit and performance statistics.

Key files: [src/happy_computing.py](src/happy_computing.py) (business logic), [src/simulation.py](src/simulation.py) (DES engine), [src/random_vars.py](src/random_vars.py) (RNG), [src/stats.py](src/stats.py) (metrics).

## Architecture
- **Template Pattern**: [Simulation](src/simulation.py) class provides the DES loop; [HappyComputingSimulation](src/happy_computing.py) implements domain logic.
- **Event System**: Immutable [Event](src/event.py) objects in a min-heap [EventQueue](src/event_queue.py).
- **Entities**: [Client](src/entities.py), Seller, Technician, ServiceType enum.
- **Resources**: 2 sellers, 3 technicians, 1 specialized technician with separate queues.

## Key Conventions
- **Naming**: Events in UPPER_CASE (ARRIVAL, SELLER_END); classes PascalCase; methods/attributes snake_case.
- **RNG**: Use seeded random for reproducibility (e.g., seed=42 for single runs).
- **Statistics**: Collect profit, wait times, service times; compute 95% confidence intervals.
- **Service Flow**: Clients go seller → technician for repairs; seller only for sales; specialized tech for changes.

## Build and Test Commands
- Install: `pip install -r requirements.txt`
- Run simulation: `python main.py` (100 runs of 480 minutes each)
- Test RNG: `python -m pytest tests/test_random_vars.py -v`
- Debug: `python src/debug_simulator.py` or `python src/debug_service_types.py`

## Common Pitfalls
- Multi-stage clients: Track wait times separately per stage; sum at departure.
- Service time conflation: Separate seller and technician times.
- Queue growth: Ensure arrival rate ≤ service rate on average.
- Confidence intervals: Uses z-critical for n=100; consider t-critical for smaller samples.

## Documentation Links
- [README.md](README.md): Installation and usage.
- [plan.md](plan.md): Project rationale.
- [Funcionamiento.md](Funcionamiento.md): Component walkthroughs (Spanish).
- [analisis-proyecto-eventos-discretos.md](analisis-proyecto-eventos-discretos.md): Problem analysis.

## Code Change Guidelines
Cada cambio que se haga debe explicarse con rigurosidad. Provide detailed explanations for modifications, including why the change is necessary, how it affects the simulation logic, and any potential impacts on statistics or performance. For example, when modifying event handlers, explain the state transitions and queue behaviors affected.</content>
<parameter name="filePath">/home/nebur02/Documents/3er Ano/2do SEMESTRE/Simulacion/Proyecto1_Eventos_Discretos/AGENTS.md