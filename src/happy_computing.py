from simulation import Simulation
from entities import Client, Seller, Technician, ServiceType
from random_vars import RandomVars
from stats import Stats
from collections import deque

class HappyComputingSimulation(Simulation):
    def __init__(self, seed=None):
        super().__init__()
        self.random = RandomVars(seed)
        self.stats = Stats()

        # Resources
        self.sellers = [Seller(i) for i in range(2)]
        self.technicians = [Technician(i) for i in range(3)]
        self.specialized_technician = Technician(0, specialized=True)

        # Queues
        self.seller_queue = deque()
        self.technician_queue = deque()
        self.specialized_queue = deque()

        # Parameters
        self.arrival_rate = 1/20  # 20 min mean
        self.repair_rate = 1/20   # 20 min mean
        self.change_rate = 1/15  # 15 min mean
        self.service_mu = 5
        self.service_sigma = 2
        self.service_probs = [0.45, 0.25, 0.10, 0.20]  # warranty repair, no warranty, change, sale
        self.profits = [0, 350, 500, 750]

        # Schedule first arrival
        self.schedule(self.random.exponential(self.arrival_rate), 'ARRIVAL')

    def handle_event(self, event):
        if event.kind == 'ARRIVAL':
            self.handle_arrival()
        elif event.kind == 'SELLER_END':
            self.handle_seller_end(event.payload)
        elif event.kind == 'TECHNICIAN_END':
            self.handle_technician_end(event.payload)
        elif event.kind == 'SPECIALIZED_END':
            self.handle_specialized_end(event.payload)

    def handle_arrival(self):
        # Create client
        service_type = ServiceType(self.random.discrete(self.service_probs))
        client = Client(self.clock, service_type)

        # Route based on service type
        if service_type in [ServiceType.REPAIR_WARRANTY, ServiceType.REPAIR_NO_WARRANTY, ServiceType.SALE_REPAIRED]:
            # Goes to seller
            self.assign_to_seller(client)
        elif service_type == ServiceType.EQUIPMENT_CHANGE:
            # Goes to specialized technician
            self.assign_to_specialized(client)

        # Schedule next arrival
        self.schedule(self.random.exponential(self.arrival_rate), 'ARRIVAL')

    def assign_to_seller(self, client):
        free_seller = next((s for s in self.sellers if not s.busy), None)
        if free_seller:
            self.start_seller_service(free_seller, client)
        else:
            self.seller_queue.append(client)

    def start_seller_service(self, seller, client):
        seller.busy = True
        seller.current_client = client
        client.service_start_time = self.clock
        service_time = self.random.normal_box_muller(self.service_mu, self.service_sigma)
        self.schedule(service_time, 'SELLER_END', seller.id)

    def handle_seller_end(self, seller_id):
        seller = self.sellers[seller_id]
        client = seller.current_client
        client.departure_time = self.clock
        self.stats.add_profit(self.profits[client.service_type.value])
        self.stats.increment_clients()
        seller.busy = False
        seller.current_client = None

        # Check if client needs technician
        if client.service_type in [ServiceType.REPAIR_WARRANTY, ServiceType.REPAIR_NO_WARRANTY]:
            self.assign_to_technician(client)
        # For SALE_REPAIRED, done

        # Serve next in queue
        if self.seller_queue:
            next_client = self.seller_queue.popleft()
            self.start_seller_service(seller, next_client)

    def assign_to_technician(self, client):
        free_tech = next((t for t in self.technicians if not t.busy), None)
        if free_tech:
            self.start_technician_service(free_tech, client)
        else:
            self.technician_queue.append(client)

    def start_technician_service(self, technician, client):
        technician.busy = True
        technician.current_client = client
        service_time = self.random.exponential(self.repair_rate)
        self.schedule(service_time, 'TECHNICIAN_END', technician.id)

    def handle_technician_end(self, technician_id):
        technician = self.technicians[technician_id]
        client = technician.current_client
        # After repair, client is done
        technician.busy = False
        technician.current_client = None

        # Serve next
        if self.technician_queue:
            next_client = self.technician_queue.popleft()
            self.start_technician_service(technician, next_client)

    def assign_to_specialized(self, client):
        if not self.specialized_technician.busy:
            self.start_specialized_service(self.specialized_technician, client)
        else:
            self.specialized_queue.append(client)

    def start_specialized_service(self, technician, client):
        technician.busy = True
        technician.current_client = client
        service_time = self.random.exponential(self.change_rate)
        self.schedule(service_time, 'SPECIALIZED_END', technician.id)

    def handle_specialized_end(self, technician_id):
        technician = self.specialized_technician
        client = technician.current_client
        technician.busy = False
        technician.current_client = None

        # Serve next
        if self.specialized_queue:
            next_client = self.specialized_queue.popleft()
            self.start_specialized_service(technician, next_client)

    def run_simulation(self, duration):
        self.run(duration)
        return self.stats