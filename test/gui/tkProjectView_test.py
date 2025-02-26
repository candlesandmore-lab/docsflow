import unittest


# Python tkinter hello world program 
# build upon: https://pythonassets.com/posts/treeview-in-tk-tkinter/
#  https://www.pythontutorial.net/tkinter/tkinter-mvc/
#  Example MVC: https://nazmul-ahsan.medium.com/how-to-organize-multi-frame-tkinter-application-with-mvc-pattern-79247efbb02b

from tkinter import END, Tk
from tkinter import ttk

from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.flows.status.trafficLightState import TrafficLightStatusColor
from test.meta.json_meta_test import TestJsonMeta


class ProjectViewTest(unittest.TestCase):

    def addNodeToTreeview(self, treeview : ttk.Treeview, parent : str, node : BaseNodeWithState) -> ttk.Treeview:
        if not isinstance(node, BaseNodeWithState):
            thisTreeItem = treeview.insert(
                parent=parent,
                index=END,
                text=node.name,
                values=(
                    "ERR",
                    "ERR"
                ))
            
        else:
            thisTreeItem = treeview.insert(
                parent=parent,
                index=END,
                text=node.name,
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
                        index=END,
                        text=node.name,
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

        return treeview

    def test_Project(self):
        pvHelper = TestJsonMeta() 
        projectNode = pvHelper.test_importProjectWithMetaDataTrafficLight()

        root = Tk()
        root.title("Treeview in Tk")
        treeview = ttk.Treeview(columns=("state", "status"))
        treeview.heading("#0", text="elment")
        treeview.heading("state", text="state (float)")
        treeview.heading("status", text="status")
        # Add tree
        self.addNodeToTreeview(
            treeview=treeview,
            node=projectNode,
            parent=""
        )
        '''
        treeview.insert(
            "",
            END,
            text="README.txt",
            values=("850 bytes", "18:30")
        )
        '''
        treeview.pack(
            fill='both', expand="yes"
        )
        root.mainloop()

    def test_Structure(self):  
        
        root = Tk()
        root.title("Treeview in Tk")
        treeview = ttk.Treeview(columns=("size", "lastmod"))
        treeview.heading("#0", text="File")
        treeview.heading("size", text="Size")
        treeview.heading("lastmod", text="Last modification")
        treeview.insert(
            "",
            END,
            text="README.txt",
            values=("850 bytes", "18:30")
        )
        treeview.pack()
        root.mainloop()

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
