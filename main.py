import time
import Tkinter as tk
import os
import re
import tkFileDialog as filedialog


from sub.process import Process


class Main(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.table = Table(self,3, 5, num_button=3)
		self.table.pack(side="top", fill="x")
		self.processes = []
		self.table.set(0, 0, "Processes/Job Order")
		self.table.set(0, 1, "Arrival")
		self.table.set(0, 2, "CPU Burst Time")
		self.table.set(0, 3, "Priority")
		self.table.set(0, 4, "Waiting Time")
		self.table.set(1, 0, "PROCESSdfasdfasdfasf 1")
		self.table.set(1, 0, "PROCESS 2", append=True)

	def clear_all(self):
		self.processes = []

	def load_file(self, filename):
		self.clear_all()
		f = open(filename, 'r')
		lines = f.readlines()[1:]
		for line in lines:
			line = re.findall(r"[^\W\d_]+|\d+", line)
			process = Process(name=line[0], arrival=int(line[1]),
							  burst=int(line[2]), priority=int(line[3]))
			self.processes.append(process)
		print(len(self.processes))

	def run(self):
		self.after(1000, self.run)


class Table(tk.Frame):
	def __init__(self, parent, rows=10, columns=2, num_button=1):
		tk.Frame.__init__(self, parent, background="#34495e")
		self._widgets = []
		self.parent = parent
		self.rows = rows
		self.columns = columns
		for row in xrange(1, rows):
			current_row = []
			for column in range(columns):
				label = tk.Label(self, text="",
								borderwidth=1, width=10, foreground="black", background="white")
				label.grid(row=row, column=column, sticky="nsew", padx=0.5, pady=0.5)
				current_row.append(label)
			self._widgets.append(current_row)

		button = tk.Button(self, text ="Load Dataset", command=self.open_file)
		button.grid(row=0, column=2, sticky="nsew", padx=0.5, pady=0.5)

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

main = Main()
main.after(10, main.run)
main.mainloop()
