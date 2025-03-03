import tkinter as tk
from tkinter import ttk

from python.flows.docsFlow.contextNode import ContextNode
from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.flows.status.trafficLightState import TrafficLightStatusColor
from python.gui.projectTreeView import ProjectTreeView

def getGUIStatusColor(status : TrafficLightStatusColor) -> str:
    result = "grey"
    if status == TrafficLightStatusColor.GREEN:
        result = "green"
    elif status == TrafficLightStatusColor.ORANGE:
        result = "orange"
    elif status == TrafficLightStatusColor.YELLOW:
        result = "yellow"
    elif status == TrafficLightStatusColor.RED:
        result = "red"
    
    return result

class NodeView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.nodeData = None

        style = ttk.Style(self)
        style.configure('NodeDetailFrame.TFrame', background='blue')
        self.config(style='NodeDetailFrame.TFrame')

        self.contextBoxes = ContextBoxes(
            self
        )
        self.contextBoxes.grid(row=0, column=0) 
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        #self.contextBoxes.pack(padx=10, pady=10, anchor=tk.CENTER)

        self.contextDetails = ContextDetails(
            self
        )
        self.contextDetails.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.rowconfigure(1, weight=8)

        #self.contextDetails.pack(padx=10, pady=10, anchor=tk.CENTER)
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
        
        #self.rowconfigure(1)
        #self.columnconfigure(1)
        
        # TODO: design the view and implement it with refresh and entry of data

    def refreshTop(self) -> None:
        
        if isinstance(self.nodeData, ContextNode):
            self.contextBoxes.grid_forget()
            self.contextBoxes.parentContext = self.nodeData
            self.contextBoxes.refresh()
            # clear details
            self.contextDetails.grid_forget()
        else:
            self.contextBoxes.grid_forget()
            self.contextDetails.grid_forget()

        self.contextBoxes.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") # pack(padx=10, pady=10, anchor=tk.CENTER, expand=True, fill='both')

    def refreshDetails(self, parentContext : BaseNodeWithState) -> None:
        
        if isinstance(self.nodeData, ContextNode):
            self.contextDetails.grid_forget()
            self.contextDetails.refresh(parentContext)

        else:
            self.contextBoxes.grid_forget()
            self.contextDetails.grid_forget()

        self.contextDetails.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")# pack(padx=10, pady=10, anchor=tk.CENTER, expand=True, fill='both')
        #leftFrame.pack(side=LEFT, expand=True, fill='both')

class ContextDetails(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # STATE view, no activity
        self.initState = "INITIALIZED"

        style = ttk.Style(self)
        style.configure('ContextDetails.TFrame', background='grey')
        self.config(style='ContextDetails.TFrame')

        # TOP level status with traffic light color
        self.stateView = tk.Label(
            self, 
            text="", 
            fg="black", 
            font=("Helvetica", 16))
        self.stateView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # PLAN view: add-update-remove
        self.planView = PlanView(self)
        self.planView.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # ACTIONS:
        self.addSubContextButton = ttk.Button(
            self,
            text="Add sub-context"
        )
        self.addSubContextButton.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # DOC view
        self.treeViewFrame = ProjectTreeView(self)
        self.treeViewFrame.grid(row=1, rowspan=2, column=2, padx=5, pady=5, sticky="nsew")
        self.rowconfigure(1, weight=1)

        # HISTORY view
        self.historyView = HistoryView(self)
        self.historyView.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    
    # 
    def refresh(self, parentContext : BaseNodeWithState) -> None:
        self.parentContext = parentContext

        stateFloat = self.parentContext.state
        statusExist, statusColorWithReasoning = self.parentContext.getStatus(
            key='TrafficLight', 
            default=(TrafficLightStatusColor.RED, "UNDEF")
        )

        if not statusExist or not isinstance(statusColorWithReasoning[0], TrafficLightStatusColor):
            stateText = "UNDEF ({})".format(stateFloat)
            statusGUIColor = getGUIStatusColor(TrafficLightStatusColor.RED)
        else:
            stateText = "{}".format(stateFloat)
            statusGUIColor = getGUIStatusColor(statusColorWithReasoning[0])

        self.stateView.config(
            text=stateText,
            bg=statusGUIColor
        )

        self.treeViewFrame.refresh(self.parentContext) # TODO: show childs only and only DOCs
        self.planView.refresh(self.parentContext)
        self.historyView.refresh(self.parentContext)
        # use the view (and not the full frame) !?

class PlanView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)



        style = ttk.Style(self)
        style.configure('PlanView.TFrame', background='grey')
        self.config(style='PlanView.TFrame')

    def refresh(self, parentContext : BaseNodeWithState) -> None:
        # TODO: read plan and present in table
        self.parentContext = parentContext
        pass

class HistoryView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        style = ttk.Style(self)
        style.configure('HistoryView.TFrame', background='pink')
        self.config(style='HistoryView.TFrame')

    def refresh(self, parentContext : BaseNodeWithState) -> None:
        # TODO: read plan and present in table
        self.parentContext = parentContext
        pass

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
                        name="{}".format(child.uuid)
                    )
                    newButton.grid(row=0, column=btIndex, padx=5, pady=5, sticky=(tk.N,tk.W,tk.E,tk.S))
                    self.buttons.append(newButton)
                    self.columnconfigure(btIndex, weight=1) # stretch button widget, all with same size
                    btIndex = btIndex + 1
            #self.rowconfigure(1)
            self.rowconfigure(0, weight=1) # stretch vertical to fill parent
            #self.columnconfigure(btIndex)
