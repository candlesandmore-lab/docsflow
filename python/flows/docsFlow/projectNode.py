
from python.elements.baseNode import NodeType
from python.flows.docsFlow.contextNode import ContextNode


class ProjectNode(ContextNode):
    def __init__(self, name:str, nodeType:NodeType):
        super().__init__(name, nodeType)
        
    def isValid(self):
        return super().isValid()
    

