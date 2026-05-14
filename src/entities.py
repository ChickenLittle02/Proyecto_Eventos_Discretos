from enum import Enum

class ServiceType(Enum):
    REPAIR_WARRANTY = 0  # $0
    REPAIR_NO_WARRANTY = 1  # $350
    EQUIPMENT_CHANGE = 2  # $500
    SALE_REPAIRED = 3  # $750

class Client:
    def __init__(self, arrival_time, service_type):
        self.arrival_time = arrival_time
        self.service_type = service_type
        self.service_start_time = None
        self.departure_time = None

class Seller:
    def __init__(self, id):
        self.id = id
        self.busy = False
        self.current_client = None

class Technician:
    def __init__(self, id, specialized=False):
        self.id = id
        self.specialized = specialized
        self.busy = False
        self.current_client = None