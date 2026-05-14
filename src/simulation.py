from event_queue import EventQueue
from event import Event

class Simulation:
    def __init__(self):
        self.clock = 0.0
        self.event_queue = EventQueue()
        self.stats = {}

    def schedule(self, delay, kind, payload=None):
        self.event_queue.push(Event(self.clock + delay, kind, payload))

    def run(self, until):
        while not self.event_queue.is_empty():
            event = self.event_queue.pop()
            if event.time > until:
                break
            self.clock = event.time
            self.handle_event(event)

    def handle_event(self, event):
        # To be overridden in subclasses
        raise NotImplementedError("Subclasses must implement handle_event")