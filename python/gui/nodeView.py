import tkinter as tk
from tkinter import LabelFrame, ttk

from python.flows.status.baseNodeWithState import BaseNodeWithState

class NodeView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.nodeData = None

        style = ttk.Style(self)
        style.configure('NodeView.TFrame', background='blue')
        self.config(style='NodeDetailFrame.TFrame')


        
        self.labelFrame = ttk.Frame(self)
        self.labelFrame.grid(row=0, column=0) 
        self.label = ttk.Label(self.labelFrame, text='Need to be initialized ...')
        self.label.pack(padx=10, pady=10, anchor=tk.CENTER)
        
        # LabelFrame is only visible if there is anything in it
        self.opsFrame = LabelFrame(
            self, text="Operations", bg="green", 
            fg="white", padx=15, pady=15)
        self.saveBt = ttk.Button(
            self.opsFrame,
            text="Save",
        )
        self.saveBt.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.quitBt = ttk.Button(
            self.opsFrame,
            text="Quit",
        )
        self.quitBt.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.opsFrame.grid(row=1, column=0) 

        self.detailsFrame = LabelFrame(
            self, text="Details", bg="grey", 
            fg="white", padx=15, pady=15)
        self.opsFrame.grid(row=2, column=0) 

        # TODO: design the view and implement it with refresh and entry of data

    def refresh(self) -> None:
        
        if self.nodeData is None:
            labelText = "Unknown"
        elif isinstance(self.nodeData, BaseNodeWithState):
            labelText = self.nodeData.name
        else:
            labelText = "Invalid object"

        self.label.pack_forget()
        self.label = ttk.Label(
            self.labelFrame,
            text='{}'.format(labelText)
        )
        self.label.pack(padx=10, pady=10, anchor=tk.CENTER)
        
 