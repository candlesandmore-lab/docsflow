from typing import Any
from python.data.baseNodeFactory import BaseNodeFactory
from python.flows.docsFlow.contextNode import ContextNode  # noqa: F401
from python.flows.docsFlow.projectNode import ProjectNode  # noqa: F401
from python.flows.docsFlow.docNode import DocNode  # noqa: F401

class DocFlowNodeFactory(BaseNodeFactory):
    def __init__(self):
        super().__init__()

    def constructNode(self, nodeType : str) -> Any:
        result = eval(nodeType)("", self)
        result.setNodeType(nodeType)

        return result
