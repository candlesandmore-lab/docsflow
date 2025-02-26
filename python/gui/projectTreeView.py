

import tkinter as tk
from tkinter import ttk
from typing import Any

from python.flows.docsFlow.contextNode import ContextNode
from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.flows.status.trafficLightState import TrafficLightStatusColor


class ProjectTreeView(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.projectData = None

        self.treeview = ttk.Treeview(self, columns=("state", "status"))
        self.treeview.heading("#0", text="elment")
        self.treeview.heading("state", text="state (float)")
        self.treeview.heading("status", text="status")

    def refresh(self) -> None:
        # Refresh tree
        self.treeview.delete(*self.treeview.get_children())

        # use data and render
        self.addNodeToTreeview(
            treeview=self.treeview,
            node=self.projectData,
            parent=""
        )
 
        self.treeview.pack(
            fill='both', expand=True
        )
        '''
        tree_view = ttk.Treeview(self)
        tree_view.pack()
        tree_view.insert('', '0', 'item1', text='PRODUCT')
 
        tree_view.insert('item1', '0', 'A', text='A')
 
        tree_view.insert('item1', '1', 'B', text='B')
        tree_view.insert('item1', '2', 'C', text='C')
        tree_view.insert('item1', '3', 'D', text='D')
        tree_view.insert('', '1', 'item2', text='REPORTS')
 
        tree_view.insert('', '3', 'item3', text='QUERIES')
        tree_view.config(height=100)
        '''


    def addNodeToTreeview(self, treeview : ttk.Treeview, parent : str, node : Any) -> ttk.Treeview:
        if  isinstance(node, ContextNode):
            thisTreeItem = treeview.insert(
                parent=parent,
                index=tk.END,
                text=node.name,
                iid=node.uuid,
                values=(
                    "{}".format(node.state),
                    "{}".format(node.getStatus(
                        key="TrafficLight", 
                        default=TrafficLightStatusColor.UNDEF
                )))
            )
            for child in node.childs:
                treeview = self.addNodeToTreeview(
                    treeview=treeview,
                    parent=thisTreeItem,
                    node = child
                )                
        '''
        if not isinstance(node, BaseNodeWithState):
            thisTreeItem = treeview.insert(
                parent=parent,
                index=tk.END,
                text=node.name,
                iid=node.name,
                values=(
                    "ERR",
                    "ERR"
                ))
            
        else:
            thisTreeItem = treeview.insert(
                parent=parent,
                index=tk.END,
                text=node.name,
                iid=node.name,
                values=(
                    "{}".format(node.state),
                    "{}".format(node.getStatus(
                        key="TrafficLight", 
                        default=TrafficLightStatusColor.UNDEF
                )))
            )
            for child in node.childs:
                if not isinstance(child, BaseNodeWithState):
                    thisTreeItem = treeview.insert(
                        parent=parent,
                        index=tk.END,
                        text=node.name,
                        iid=node.name,
                        values=(
                            "ERR",
                            "ERR"
                        ))                
                else:
                    treeview = self.addNodeToTreeview(
                        treeview=treeview,
                        parent=thisTreeItem,
                        node = child
                    )
        '''
        return treeview