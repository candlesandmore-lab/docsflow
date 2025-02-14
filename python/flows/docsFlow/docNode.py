
import os
from python.elements.baseNode import BaseNode, NodeReturnValue, NodeType


class DocNode(BaseNode):
    def __init__(self, name:str, nodeType:NodeType):
        super().__init__(name, nodeType)
        
    def setDocPath(self, path:str) -> None:
        self.properties['docPath'] = path

    def isValid(self) -> bool:
        result : bool = super().isValid()
        if result:
            if 'docPath' in self.properties.keys():
                if os.path.isfile(self.properties['docPath']):
                    result = True
                else:
                    self.logger.error("Doc [{}] is not a file.".format(
                        self.properties['docPath']
                    ))
            else:
                self.logger.error("Doc has not 'docPath' property.")

        return result

    def refreshProperties(self) -> NodeReturnValue:
        retValue = NodeReturnValue.OK

        if not self.isValid():
            retValue = NodeReturnValue.FAILURE
        else:
            stats = os.stat(self.properties['docPath'])
            self.properties['size'] = stats.st_size
            self.properties['owner'] = stats.st_uid
            self.properties['size'] = stats.st_size
            self.properties['mupdateTime'] = os.path.getmtime(self.properties['docPath'])
            self.properties['createTime'] = os.path.getctime(self.properties['docPath'])

        return retValue
        

