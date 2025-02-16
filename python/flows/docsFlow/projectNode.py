
from python.data.dataFactory import DataFactory
from python.elements.baseNode import NodeType
from python.flows.docsFlow.contextNode import ContextNode


class ProjectNode(ContextNode):
    def __init__(self, name:str, factory : DataFactory):
        super().__init__(
            name=name, 
            factory=factory)

        self.nodeType = NodeType.PROJECT

        # TODO: set default values for properties, such that stepwise constructed nodes have all props
        
    def isValid(self):
        return super().isValid()
    

