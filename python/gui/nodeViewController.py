
from python.gui.model import Model
from python.gui.nodeView import ContextBoxes
from python.gui.view import View


class NodeViewController():
    def __init__(self, model : Model, view : View) -> None:
        self.model = model
        self.view = view
        self._bind()

    def _bind(self):
        # TODO: bind selection in tree to to nodeSelected
        if isinstance(self.view.frames['details'].contextBoxes, ContextBoxes):
            
            for button in self.view.frames['details'].contextBoxes.buttons:
                #button.config(command=lambda t=button['text']: self.contextSelected(t))
                button.config(command=lambda t=button._name: self.contextSelected(t))

    def contextSelected(self, contextName):
        print("*DEB* : selected [{}]".format(contextName))
        newDetailedFocusNode = self.model.projectModel.getNodeByUUID(contextName)
        self.view.frames['details'].contextDetails.parentContext = newDetailedFocusNode
        self.view.frames['details'].refreshDetails()

    def parentChanged(self, newFocusNode):
        self.view.frames['details'].nodeData = newFocusNode
        self.view.frames['details'].refreshTop()
        self._bind()

    def setProjectNode(self, model : Model) -> None:
        self.parentChanged(self.model.projectModel.projectNode)

