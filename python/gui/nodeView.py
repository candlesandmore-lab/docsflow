import tkinter as tk
from tkinter import ttk

from python.flows.status.baseNodeWithState import BaseNodeWithState

class NodeView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.nodeData = None

    def refresh(self) -> None:
        style = ttk.Style(self)
        style.configure('NodeView.TFrame', background='blue')
        self.config(style='NodeDetailFrame.TFrame')
        if self.nodeData is None:
            labelText = "Unknown"
        elif isinstance(self.nodeData, BaseNodeWithState):
            labelText = self.nodeData.name
        else:
            labelText = "Invalid object"

        label = ttk.Label(self, text='{}'.format(
            labelText
        ))
        label.pack(padx=10, pady=10, anchor=tk.CENTER)
 