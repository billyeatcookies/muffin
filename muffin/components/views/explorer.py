import os
import tkinter as tk
from tkinter import ttk

from ..utils import DirectoryTreeWatcher
from .view import View


class Explorer(View):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.symbol = "🔷"

        self.tree = ttk.Treeview(self)
        self.tree.config(show="tree", columns=('path'))
        self.tree.pack(fill=tk.BOTH, side=tk.LEFT)

        style = ttk.Style()
        style.theme_use('default')
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])

        self.watcher = DirectoryTreeWatcher(self.tree)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(fill=tk.Y, side=tk.LEFT, padx=(1, 0))
    
        self.tree.bind('<Double-1>', self.openfile)

    def openfile(self, event):
        item = self.tree.focus()
        path = self.tree.set(item, 'path')

        if os.path.isfile(path):
            self.master.master.editor.openfile(path)
