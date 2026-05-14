class Event:
    def __init__(self, time, kind, payload=None):
        self.time = time
        self.kind = kind
        self.payload = payload

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"Event(time={self.time}, kind={self.kind}, payload={self.payload})"