

from python.gui.tkRoot import TkRoot


class View:
    def __init__(self):
        self.root = TkRoot()
        
        self.frames = {
            "tree" : self.root.tree_view_frame, #ProjectTreeView
            "details": self.root.display_frame  #NodeView
        }
        

    '''
    def switch(self, name):
        new_frame = self.frame_classes[name](self.root)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    '''

    def startMainloop(self):
        self.root.mainloop()