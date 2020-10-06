import tkinter as tk
import random_walker


class WalkerApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.count_entry = tk.Entry()
        self.count_entry.pack()

        self.run_button = tk.Button(self)
        self.run_button["text"] = "Run walk"
        self.run_button["command"] = lambda: random_walker.run_walk(int(self.count_entry.get()))
        self.run_button.pack()


root = tk.Tk()
myapp = WalkerApp(root)
myapp.mainloop()
