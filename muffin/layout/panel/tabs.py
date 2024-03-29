import tkinter as tk

from .tab import Tab


class Tabs(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.config(bg='#ececec')

        self.holder = tk.Frame(self, bg="#a0a0a0")
        self.holder.pack(fill=tk.Y, side=tk.LEFT)

        self.tabs = []

    def add_tab(self, view):
        tab = Tab(self.holder, self, view)
        tab.pack(fill=tk.Y, side=tk.LEFT, padx=(0, 1))
        self.tabs.append(tab)
    
    def set_active_tab(self, view):
        for tab in self.tabs:
            if tab.view != view:
                tab.deselect()
        self.master.set_active_view(view)
