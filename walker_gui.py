import tkinter as tk
from tkinter import scrolledtext
import random_walker


class WalkerApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, pad=3, weight=1)
        self.columnconfigure(1, pad=3, weight=1)
        self.rowconfigure(0, pad=3, weight=1)
        self.rowconfigure(1, pad=3, weight=1)
        self.rowconfigure(2, pad=3, weight=1)
        self.rowconfigure(3, pad=3, weight=1)

        self.movies_label = tk.Label(text="Names of movies, one movie per line")
        self.movies_label.grid(row=0, column=0, sticky=tk.EW)
        self.movies = scrolledtext.ScrolledText()
        self.movies.grid(row=1, column=0, sticky=tk.EW)

        self.weights_label = tk.Label(text="Weight of each movie, one int per line")
        self.weights_label.grid(row=0, column=1, sticky=tk.EW)
        self.weights = scrolledtext.ScrolledText()
        self.weights.grid(row=1, column=1, sticky=tk.EW)

        self.run_button = tk.Button()
        self.run_button["text"] = "Run walk"
        self.run_button["command"] = self.run_button_command
        self.run_button.grid(row=2, columnspan=2)

        self.out_var = tk.StringVar()
        self.out_label = tk.Message(textvariable=self.out_var, width=500)
        self.out_label.grid(row=3, columnspan=2)
        self.out_var.set("Your recommendations come here")

    def run_button_command(self):
        weights = [int(x) for x in self.weights.get('1.0', tk.END).split('\n')[:-1]]
        total = sum(weights)
        weights = [x / total for x in weights]

        self.out_var.set('\n'.join(random_walker.run_walk(
            self.movies.get('1.0', tk.END).split('\n')[:-1],
            weights)))


root = tk.Tk()
root.resizable(False, False)
myapp = WalkerApp(root)
myapp.mainloop()
