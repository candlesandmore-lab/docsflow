from typing import Any
from python.data.dataFactory import DataFactory
from python.elements.baseNode import BaseNode  # noqa: F401

class BaseNodeFactory(DataFactory):
    def __init__(self):
        super().__init__()

    def constructNode(self, nodeType : str) -> Any:
        result = eval(nodeType)("", self)
        result.setNodeType(nodeType)

        return result
