from typing import Any

class DataFactory():
    def __init__(self):
        pass

    def constructNode(self, nodeType : str) -> Any:
        result = eval(nodeType)("", self)
        result.setNodeType(nodeType)

        return result


        