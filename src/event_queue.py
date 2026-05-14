import heapq
from event import Event

class EventQueue:
    def __init__(self):
        self.queue = []

    def push(self, event):
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        return self.queue[0] if self.queue else None