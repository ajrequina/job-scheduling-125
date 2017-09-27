

class Process(object):
    def __init__(self, name=None, arrival=0, burst=0, priority=0):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

    def decrease_burst(self, factor=1):
        if self.burst:
            self.burst -= 1
