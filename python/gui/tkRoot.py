import tkinter as tk
from tkinter import ttk

from python.gui.nodeView import NodeView
from python.gui.projectTreeView import ProjectTreeView

class TkRoot(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Test')
        self.iconbitmap()
        self.state('zoomed')
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)

        self.tree_view_frame = ProjectTreeView(
            paned_window, width=75, height=300, relief=tk.SUNKEN)
        '''
        moved to project tree controller
        self.tree_view_frame.tree_view.bind(
            '<<TreeviewSelect>>', self.on_tree_view_select)
        '''
        self.display_frame = NodeView(
            paned_window, width=400, height=300, relief=tk.SUNKEN)
        
        paned_window.add(self.tree_view_frame, weight=0)
        paned_window.add(self.display_frame, weight=4)
        paned_window.pack(fill=tk.BOTH, expand=True)
 
    def on_tree_view_select(self, event):
        frame_id = self.tree_view_frame.tree_view.selection()
        self.display_frame.change_frame(frame_id)
 
 