import copy

class Algorithm(object):
    def __init__(self, name=None, processes=[], awt=0, unit="ms", time_slice=4):
        self.name = name
        self.processes = processes
        self.awt = awt
        self.unit = unit
        self.queue = []
        self.time_slice = time_slice
        self.total_burst = 0

        self.get_total_burst()
        self.perform()

    def get_total_burst(self):
        for process in self.processes:
            self.total_burst += process.burst

    def perform(self):
        if self.name == "FCFS":
            self.fcfs()
        elif self.name == "SJF":
            self.sjf()
        elif self.name == "PRIORITY":
            self.priority()
        elif self.name == "RROBIN":
            self.round_robin()

    def fcfs(self):
        self.processes = sorted(self.processes, key=lambda x: x.order, reverse=False)
        current_time = 0
        total_waiting = 0
        for process in self.processes:
            process.start = current_time
            process.end = current_time + process.burst
            process.waiting = current_time
            current_time = current_time + process.burst
            total_waiting += process.waiting
            self.queue.append(process)

        self.awt = total_waiting / len(self.processes)

    def sjf(self):
        self.processes = sorted(self.processes, key=lambda x: x.order, reverse=False)
        self.processes = sorted(self.processes, key=lambda x: x.burst, reverse=False)
        current_time = 0
        total_waiting = 0
        for process in self.processes:
            process.start = current_time
            process.end = current_time + process.burst
            process.waiting = current_time
            current_time = current_time + process.burst
            total_waiting += process.waiting
            self.queue.append(process)
        self.awt = total_waiting / len(self.processes)

    def priority(self):
        self.processes = sorted(self.processes, key=lambda x: x.order, reverse=False)
        self.processes = sorted(self.processes, key=lambda x: x.priority, reverse=False)
        current_time = 0
        total_waiting = 0
        for process in self.processes:
            process.start = current_time
            process.end = current_time + process.burst
            process.waiting = current_time
            current_time = current_time + process.burst
            total_waiting += process.waiting
            self.queue.append(process)
        self.awt = total_waiting / len(self.processes)

    def round_robin(self):
        self.processes = sorted(self.processes, key=lambda x: x.order, reverse=False)
        tick = 0
        idx = 0
        current_time = 0
        total_waiting = 0
        not_done = len(self.processes) - 1
        done_processes = []

        while not_done:
            process = self.processes[idx]
            process.start = current_time

            if current_time % self.time_slice != 0:
                process.decrease_burst(factor=(current_time % self.time_slice))
                process.end = current_time + (current_time % self.time_slice)
                current_time += (current_time % self.time_slice)
            else:
                process.decreas

            process.decrease_burst(factor=self.time_slice)
            if process.counter
        while tick <= self.total_burst:
            process = self.processes[idx]
            process.decrease_burst()
            if process.is_done() or (tick > 0  and tick % self.time_slice == 0):
                process.executions += self.time_slice
                process.start = start
                process.end = tick
                self.queue.append(copy.deepcopy(process))
                if process.is_done():
                    process.waiting = tick - process.executions
                    total_waiting += tick - process.executions

                idx += 1
                if idx >= len(self.processes):
                    idx = 0

            tick += 1
        self.awt = total_waiting / len(self.processes)

    def get_awt(self):
        return str(self.awt) + self.unit

    def get_gantt(self):
        gantt = ""
        start = self.processes[0].start
        for idx, process in enumerate(self.queue):
            gantt += process.name + "(" + str(start) + "-" + str(process.end) + ")"
            if idx == len(self.processes) - 1:
                gantt += ""
            else:
                gantt += ", "
            start = process.end

        return gantt
