

class Algorithm(object):
    def __init__(self, name=None, processes=[], awt=0, unit="ms"):
        self.name = name
        self.processes = processes
        self.awt = awt
        self.unit = unit
        self.queue = []
        self.perform()

    def perform(self):
        if self.name == "FCFS":
            self.fcfs()
        elif self.name == "SJF":
            self.sjf()

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

    def get_awt(self):
        return str(self.awt) + self.unit

    def get_gantt(self):
        gantt = ""
        start = self.processes[0].start
        for idx, process in enumerate(self.processes):
            gantt += process.name + "(" + str(start) + "-" + str(process.end) + ")"
            if idx == len(self.processes) - 1:
                gantt += ""
            else:
                gantt += ", "
            start = process.end

        return gantt
