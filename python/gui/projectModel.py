

from typing import Optional
from python.elements.baseNode import BaseNode
from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.gui.observableModel import ObservableModel


class ProjectModel(ObservableModel):
    def __init__(self) -> None:
        super().__init__()
        self.projectNode : BaseNodeWithState

    def setNode(self, node : BaseNodeWithState) -> None:
        self.projectNode = node
        self.trigger_event("projectNodeChanged")

    def getNodeByUUID(
            self, 
            uuid : str) -> Optional[BaseNode]:
        
        return self.getChildNodeByUUID(
            uuid=uuid,
            node=self.projectNode
        )
    
    def getChildNodeByUUID(
            self, 
            uuid : str,
            node : BaseNode) -> Optional[BaseNode]:
        
        result = None
        if node.uuid == uuid:
            result = node
        else:
            for child in node.childs:
                result = self.getChildNodeByUUID(uuid, child)
                if result is not None:
                    break

        return result
    
    def saveNode(self):
        # TODO: store in DB
        pass

    def getNode(self):
        # TODO: get from DB
        pass