
from python.elements.baseNode import BaseNode
from python.gui.model import Model
from python.gui.view import View


class ProjectTreeController():
    def __init__(self, model : Model, view : View) -> None:
        self.model = model
        self.view = view
        self._bind()

    def _bind(self):
        pass
        '''
        # TODO: bind selection in tree to to nodeSelected
        self.view.frames['tree'].treeview.bind(
            '<<TreeviewSelect>>', 
            self.nodeSelected
        )
        '''

    # TODO: bind to GUI operation
    def setProjectNode(self, model : Model) -> None:
        self.view.frames['tree'].projectData = self.model.projectModel.projectNode
        self.view.frames['tree'].refresh()


