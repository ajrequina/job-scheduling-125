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
        self.job_order = []
        self.perform()

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
            self.job_order.append([process.name, current_time, current_time + process.counter])
            process.waiting = current_time
            current_time = current_time + process.counter
            total_waiting += process.waiting

        self.awt = total_waiting / len(self.processes)

    def sjf(self):
        self.processes = sorted(self.processes, key=lambda x: x.order, reverse=False)
        self.processes = sorted(self.processes, key=lambda x: x.burst, reverse=False)
        current_time = 0
        total_waiting = 0
        for process in self.processes:
            self.job_order.append([process.name, current_time, current_time + process.counter])
            process.waiting = current_time
            current_time = current_time + process.counter
            total_waiting += process.waiting

        self.awt = total_waiting / len(self.processes)

    def priority(self):
        self.processes = sorted(self.processes, key=lambda x: x.order, reverse=False)
        self.processes = sorted(self.processes, key=lambda x: x.priority, reverse=False)
        current_time = 0
        total_waiting = 0
        for process in self.processes:
            self.job_order.append([process.name, current_time, current_time + process.counter])
            process.waiting = current_time
            current_time = current_time + process.counter
            total_waiting += process.waiting

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

                if process.counter < self.time_slice:
                    self.job_order.append([process.name, time, time + process.counter])
                    time = (time + process.counter)
                    factor = process.counter
                    process.decrease_burst(factor=process.counter)
                    process.executions += self.time_slice
                    process.end = time
                else:
                    self.job_order.append([process.name, time, time + self.time_slice])
                    time = (time + self.time_slice)
                    factor = self.time_slice
                    process.decrease_burst(factor=self.time_slice)
                    process.executions += self.time_slice

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
        processes = self.processes
        current_time = 0
        idx = 1
        current = processes[0]
        arrived_count = 1

        while current.counter > 0:
            arrived_processes = []
            for item in processes:
                if item.order != current.order and item.arrival == current_time:
                    arrived_count += 1
                    arrived_processes.append(item)

            self.job_order.append([current.name, current_time, current_time + 1])
            current.waiting = (current_time - current.executions) - current.arrival
            current.executions += 1
            current.decrease_burst(factor=1)

            if len(arrived_processes) and arrived_count != len(processes) and current.counter == 0:
                current = arrived_processes[0]

            for item in arrived_processes:
                if item.order != current.order and item.counter < current.counter:
                    current = item

            current_time += 1

        self.processes = sorted(self.processes, key=lambda x: x.counter, reverse=False)
        total_waiting = 0
        for process in self.processes:
            if process.counter > 0:
                self.job_order.append([process.name, current_time, current_time + process.counter])
                process.waiting = (current_time - process.executions) - process.arrival
                current_time = current_time + process.counter
            total_waiting += process.waiting

        self.processes = sorted(self.processes, key=lambda x: x.arrival, reverse=False)
        self.awt = total_waiting / len(self.processes)

    def get_awt(self):
        return str(self.awt) + self.unit

    def get_gantt(self):
        gantt = ""
        for idx, process in enumerate(self.job_order):
            gantt += process[0] + "(" + str(process[1]) + "-" + str(process[2]) + ")"
            if idx == len(self.job_order) - 1:
                gantt += ""
            else:
                gantt += " -- "
            if idx > 0 and idx % 5 == 0:
                gantt += "\n"

        return gantt
