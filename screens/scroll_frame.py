import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Frame):
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)

		self.canvas = tk.Canvas(self)
		self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.scrollable_frame = tk.Frame(self.canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		)

		self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.scrollbar.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)

		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
		self.canvas.bind_all("<Button-4>", self._on_mousewheel)
		self.canvas.bind_all("<Button-5>", self._on_mousewheel)
		self.canvas.bind("<Configure>", self._on_canvas_configure)

	def _on_mousewheel(self, event):
		if event.num == 4 or event.delta > 0:
			self.canvas.yview_scroll(-1, "units")
		elif event.num == 5 or event.delta < 0:
			self.canvas.yview_scroll(1, "units")
	

	def _on_canvas_configure(self, event):
		self.canvas.itemconfigure(
			self.canvas.find_withtag("all")[0],
			width=event.width
		)
