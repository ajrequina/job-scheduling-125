

class Process(object):
    def __init__(self, order=-1, name=None, arrival=0, burst=0, priority=0, waiting=0, unit="ms", executions=0):
        self.order = order
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.counter = 0
        self.priority = priority
        self.waiting = waiting
        self.unit = unit
        self.start = 0
        self.end = burst
        self.executions = executions

    def __str__(self):
        return str(self.name)

    def decrease_burst(self, factor=1):
        if self.counter < self.burst:
            self.counter -= factor

    def is_done(self):
        return self.counter == 0


    def get_arrival(self):
        return str(self.arrival) + self.unit

    def get_burst(self):
        return str(self.burst) + self.unit

    def get_priority(self):
        return str(self.priority)

    def get_waiting(self):
        return str(self.waiting) + self.unit
