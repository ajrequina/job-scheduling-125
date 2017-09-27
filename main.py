import time
import Tkinter as tk
import os
import re
import tkFileDialog as filedialog
import copy


from sub.process import Process
from sub.algorithm import Algorithm


class Main(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.table = Table(self,rows=2, columns=5)
		self.table.pack(side="top", fill="x")
		self.processes = []
		self.algorithm = {}

		self.table.set(0, 0, "Process")
		self.table.set(0, 1, "Arrival Time")
		self.table.set(0, 2, "Burst Time")
		self.table.set(0, 3, "Priority")
		self.table.set(0, 4, "Waiting Time")

	def clear_all(self):
		self.processes = []

	def load_file(self, filename):
		self.clear_all()
		f = open(filename, 'r')
		lines = f.readlines()[1:]
		for idx, line in enumerate(lines):
			line = re.findall(r"[^\W\d_]+|\d+", line)
			process = Process(order=idx, name=line[0], arrival=int(line[1]),
							  burst=int(line[2]), priority=int(line[3]))
			self.processes.append(process)

		self.algorithm["FCFS"] = Algorithm(name="FCFS", processes=copy.deepcopy(self.processes))
		self.algorithm["SJF"] = Algorithm(name="SJF", processes=copy.deepcopy(self.processes))
		self.algorithm["SRPT"] = Algorithm(name="SRPT", processes=copy.deepcopy(self.processes))
		self.algorithm["PRIORITY"] = Algorithm(name="PRIORITY", processes=copy.deepcopy(self.processes))
		self.algorithm["RROBIN"] = Algorithm(name="RROBIN", processes=copy.deepcopy(self.processes))
		self.display(processes=copy.deepcopy(self.processes))

	def display(self, processes=None, key=None):
		for idx, process in enumerate(processes):
			append = True if idx else False
			self.table.set(1, 0, process.name, append=append)
			self.table.set(1, 1, process.get_arrival(), append=append)
			self.table.set(1, 2, process.get_burst(), append=append)
			self.table.set(1, 3, process.get_priority(), append=append)
			self.table.set(1, 4, process.get_waiting(), append=append)
		if key:
			self.display_awt(key)
			self.display_gantt(key)

	def display_awt(self, key=None):
		awt = "AWT: " + self.algorithm[key].get_awt()
		self.table.set(2, 0, awt)

	def display_gantt(self, key=None):
		self.table.set(4, 0, self.algorithm[key].get_gantt())

	def display_results(self, key):
		self.display(processes=self.algorithm[key].processes, key=key)


class Table(tk.Frame):
	def __init__(self, parent, rows=10, columns=2, num_button=1):
		tk.Frame.__init__(self, parent, background="#34495e")
		self._widgets = []
		self.parent = parent
		self.rows = rows
		self.columns = columns

		for row in xrange(0, rows):
			current_row = []
			for column in range(columns):
				label = tk.Label(self, text="",
								borderwidth=1, width=15, foreground="black", background="white")
				label.grid(row=row, column=column, sticky="nsew", padx=0.5, pady=0.5)
				current_row.append(label)
			self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="AWT: 0 ms",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows, columnspan=5, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="Evaluation: FCFS (38 ms), SJF (58 ms), SRPT (60 ms), PRIORITY (80 ms), RROBIN (90 ms)",
						borderwidth=1, width=15, foreground="black", background="white", anchor="w")
		label.grid(row=rows + 1, columnspan=5, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="",
						borderwidth=1, width=15, foreground="black", background="white", wraplength=700, anchor="w")
		label.grid(row=rows + 2, columnspan=5, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		label = tk.Label(self, text="",
						borderwidth=1, width=15, foreground="#34495e", background="#34495e", anchor="w")
		label.grid(row=rows + 3, columnspan=5, sticky="nsew", padx=1, pady=1)
		current_row.append(label)
		self._widgets.append(current_row)

		current_row = []
		button = tk.Button(self, text ="FCFS", command= lambda: self.display_results("FCFS"))
		button.grid(row=rows + 4, column=0, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="SJF", command= lambda: self.display_results("SJF"))
		button.grid(row=rows + 4, column=1, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="SRPT", command=lambda: self.display_results("SRPT"))
		button.grid(row=rows + 4, column=2, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="PRIORITY", command=lambda: self.display_results("PRIORITY"))
		button.grid(row=rows + 4, column=3, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)

		button = tk.Button(self, text ="RROBIN", command=lambda: self.display_results("RROBIN"))
		button.grid(row=rows + 4, column=4, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)
		self._widgets.append(current_row)

		current_row = []
		button = tk.Button(self, text ="LOAD FILE", command=self.open_file)
		button.grid(row=rows + 5, columnspan=5, sticky="nsew", padx=0.5, pady=0.5)
		current_row.append(button)
		self._widgets.append(current_row)

		for column in range(columns):
			self.grid_columnconfigure(column, weight=1)

	def set(self, row, column, value, foreground="black", background="white", append=False):
		widget = self._widgets[row][column]
		if append:
			value = widget.cget("text") + "\n" + value
		widget.configure(text=value, foreground=foreground, background=background)

	def open_file(self):
		name= filedialog.askopenfilename()
		self.parent.load_file(filename=name)

	def display_results(self, key=None):
		self.parent.display_results(key=key)

main = Main()
main.mainloop()
