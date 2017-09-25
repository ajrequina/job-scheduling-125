import random
import time
import Tkinter as tk


class Main(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.table = Table(self, 31, 8)
		self.table.pack(side="top", fill="x")

	def run(self):
		self.after(1000, self.run)



class Table(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        tk.Frame.__init__(self, parent, background="#34495e")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="",
                                 borderwidth=1, width=10, foreground="black", background="white")
                label.grid(row=row, column=column, sticky="nsew", padx=0.5, pady=0.5)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value, foreground="black", background="white"):
        widget = self._widgets[row][column]
        widget.configure(text=value, foreground=foreground, background=background)


main = Main()
# main.after(10, main.run)
# main.mainloop()
