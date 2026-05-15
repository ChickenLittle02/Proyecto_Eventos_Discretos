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
        self.seller_end_time = None
        self.technician_start_time = None
        self.departure_time = None
        self.wait_time_in_seller_queue = 0.0
        self.wait_time_in_technician_queue = 0.0
        self.service_time_with_seller = 0.0
        self.service_time_with_technician = 0.0

class Seller:
    def __init__(self, id):
        self.id = id
        self.busy = False
        self.current_client = None
        self.busy_time = 0.0
        self.busy_start_time = None

    def start_service(self, current_time):
        self.busy = True
        self.busy_start_time = current_time

    def end_service(self, current_time):
        if self.busy_start_time is not None:
            self.busy_time += current_time - self.busy_start_time
            self.busy_start_time = None
        self.busy = False

    def finalize_busy_time(self, until):
        if self.busy and self.busy_start_time is not None:
            self.busy_time += max(0.0, until - self.busy_start_time)
            self.busy_start_time = until

class Technician:
    def __init__(self, id, specialized=False):
        self.id = id
        self.specialized = specialized
        self.busy = False
        self.current_client = None
        self.busy_time = 0.0
        self.busy_start_time = None

    def start_service(self, current_time):
        self.busy = True
        self.busy_start_time = current_time

    def end_service(self, current_time):
        if self.busy_start_time is not None:
            self.busy_time += current_time - self.busy_start_time
            self.busy_start_time = None
        self.busy = False

    def finalize_busy_time(self, until):
        if self.busy and self.busy_start_time is not None:
            self.busy_time += max(0.0, until - self.busy_start_time)
            self.busy_start_time = until