import tkinter as tk
from tkinter import LabelFrame, ttk

from python.flows.docsFlow.contextNode import ContextNode
from python.flows.status.baseNodeWithState import BaseNodeWithState

class NodeView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.nodeData = None

        style = ttk.Style(self)
        style.configure('NodeView.TFrame', background='blue')
        self.config(style='NodeDetailFrame.TFrame')

        self.contextBoxes = ContextBoxes(
            self
        )
        self.contextBoxes.grid(row=0, column=0) 
        self.contextBoxes.pack(padx=10, pady=10, anchor=tk.CENTER)

        # LabelFrame is only visible if there is anything in it
        '''
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
        self.detailsFrame.grid(row=2, column=0) 
        '''    
        # TODO: design the view and implement it with refresh and entry of data

    def refresh(self) -> None:
        
        if isinstance(self.nodeData, ContextNode):
            self.contextBoxes.pack_forget()
            self.contextBoxes.parentContext = self.nodeData
            self.contextBoxes.refresh()
        else:
            self.contextBoxes.pack_forget()

        self.contextBoxes.pack(padx=10, pady=10, anchor=tk.CENTER)
class ContextBoxes(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.parentContext = None
        self.buttons : list [ttk.Button] = []

        style = ttk.Style(self)
        style.configure('ContextBoxes.TFrame', background='green')
        self.config(style='ContextBoxes.TFrame')


    def refresh(self) -> None:
        while self.buttons:
            self.buttons.pop().grid_forget()


        if isinstance(self.parentContext, ContextNode):
            btIndex = 0
            for child in self.parentContext.childs:

                if isinstance(child, ContextNode):
                    newButton = ttk.Button(
                        self,
                        text=child.name,
                    )
                    newButton.grid(row=0, column=btIndex, padx=5, pady=5, sticky=tk.E)
                    self.buttons.append(newButton)
                    btIndex = btIndex + 1
