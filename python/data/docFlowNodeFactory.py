from typing import Any, cast
from python.data.baseNodeFactory import BaseNodeFactory
from python.elements.baseNode import BaseNode
from python.flows.docsFlow.contextNode import ContextNode  # noqa: F401
from python.flows.docsFlow.projectNode import ProjectNode  # noqa: F401
from python.flows.docsFlow.docNode import DocNode  # noqa: F401
from python.flows.docsFlow.taskNode import TaskNode # noqa: F401
from python.infra.logging import getMainLogger  # noqa: F401

class DocFlowNodeFactory(BaseNodeFactory):
    def __init__(self):
        super().__init__()
        self.logger = getMainLogger()

    def constructNode(self, nodeType : str) -> Any:
        result = eval(nodeType)("", self)
        result.setNodeType(nodeType)

        return result
    
    # called by UI
    def getChildNodeByName(self, parent : BaseNode, name : str) -> tuple[bool, BaseNode]:
        foundNode = False
        result : BaseNode = cast(BaseNode, None)
        for child in parent.childs:
            if child.name == name:
                foundNode = True
                result = child

        return foundNode, result