

from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.gui.observableModel import ObservableModel


class ProjectModel(ObservableModel):
    def __init__(self) -> None:
        super().__init__()
        self.projectNode : BaseNodeWithState

    def setNode(self, node : BaseNodeWithState) -> None:
        self.projectNode = node
        self.trigger_event("projectNodeChanged")

    def saveNode(self):
        # TODO: store in DB
        pass

    def getNode(self):
        # TODO: get from DB
        pass