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
        self.max_arrival = 0

        self.get_maxes()
        self.perform()
        self.job_order = []

    def get_maxes(self):
        for process in self.processes:
            self.total_burst += process.burst
            if process.arrival > self.max_arrival:
                self.max_arrival = process.arrival

    def perform(self):
        if self.name == "FCFS":
            self.fcfs()
        elif self.name == "SJF":
            self.sjf()
        elif self.name == "PRIORITY":
            self.priority()
        elif self.name == "RROBIN":
            self.round_robin()
        elif self.name == "SRPT":
            self.srpt()

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
        done_processes = []
        idx = 0
        time = 0
        total_waiting = 0
        factor = 0

        while len(done_processes) != len(self.processes):
            if idx not in done_processes:
                process = self.processes[idx]
                
                process.start = time
                    
                if process.counter < self.time_slice:
                    time = (time + process.counter)
                    factor = process.counter
                    process.decrease_burst(factor=process.counter)
                    process.executions += self.time_slice
                    process.end = time
                    self.queue.append(copy.deepcopy(process))
                else:
                    time = (time + self.time_slice)
                    factor = self.time_slice
                    process.decrease_burst(factor=self.time_slice)
                    process.executions += self.time_slice
                    process.end = time
                    self.queue.append(copy.deepcopy(process))

                if process.counter <= 0:
                    done_processes.append(idx)
                    process.waiting = ((time - factor) - process.executions)
                    total_waiting += ((time - factor) - process.executions)
                    
            
            idx += 1
            if idx >= len(self.processes):
                idx = 0

        self.awt = total_waiting / len(self.processes)

    def srpt(self):
        self.processes = sorted(self.processes, key=lambda x: x.arrival, reverse=False)
        processes = copy.deepcopy(self.processes)
        current_time = 0
        idx = 0
        current = None

        while current_time <= self.max_arrival:
            arrived_processes = []
            for item in processes:
                if item.counter:
                    if item.arrival == current_time:
                        arrived_processes.append(item)

            if not current:
                current = arrived_processes[0]
                
            for item in arrived_processes:
                if item.counter < current.counter:
                    current.end = current_time
                    current = item

            current.decrease_burst(factor=1)
            current.executions += 1

            if current.counter == 0:
                current = None

            current_time += 1

        processes = sorted(processes, key=lambda x: x.order, reverse=False)
        processes = sorted(processes, key=lambda x: x.burst, reverse=False)





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
