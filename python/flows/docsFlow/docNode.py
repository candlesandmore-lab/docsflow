
import json
import os
from python.data.dataFactory import DataFactory
from python.elements.baseNode import BaseNode, NodeReturnValue, NodeType
from python.elements.datetimeItem import DatetimeItem
from python.flows.docsFlow.docFlowNodeTypes import DocNodeType
from python.infra.timeStampMeta import utcDateTimeFromEpochSeconds

class DocNode(BaseNode):
    def __init__(self, name:str, factory : DataFactory):
        super().__init__(
            name=name, 
            factory=factory)

        self.docType = DocNodeType()
        
    def fromJson(
            self,
            jsonString : str
        ) -> None:
        super().fromJson(jsonString)
        
        _from_json_dict = json.loads(jsonString)
        self.docType.fromJson(
            jsonString=json.dumps(_from_json_dict['docType'])
        )

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
            self.properties['mupdateTime'] = DatetimeItem(
                when=utcDateTimeFromEpochSeconds(os.path.getmtime(self.properties['docPath']))
            )
            self.properties['createTime'] = DatetimeItem(
                when=utcDateTimeFromEpochSeconds(os.path.getctime(self.properties['docPath']))
            )

        return retValue
        

