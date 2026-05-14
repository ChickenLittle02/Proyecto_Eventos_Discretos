class Stats:
    def __init__(self):
        self.total_profit = 0
        self.clients_served = 0
        self.seller_queue_lengths = []
        self.technician_queue_lengths = []
        self.specialized_queue_lengths = []

    def add_profit(self, amount):
        self.total_profit += amount

    def increment_clients(self):
        self.clients_served += 1

    def record_queues(self, seller_q, tech_q, spec_q):
        self.seller_queue_lengths.append(len(seller_q))
        self.technician_queue_lengths.append(len(tech_q))
        self.specialized_queue_lengths.append(len(spec_q))