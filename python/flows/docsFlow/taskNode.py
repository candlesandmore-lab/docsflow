
import json
from python.data.dataFactory import DataFactory
from python.elements.baseNode import NodeReturnValue
from python.flows.docsFlow.docFlowNodeTypes import TaskNodeType
from python.flows.status.baseNodeWithStatus import BaseNodeWithStatus

class TaskNode(BaseNodeWithStatus):
    def __init__(self, name:str, factory : DataFactory):
        super().__init__(
            name=name, 
            factory=factory)

        self.taskType = TaskNodeType()
        
    def fromJson(
            self,
            jsonString : str
        ) -> None:
        super().fromJson(jsonString)
        
        _from_json_dict = json.loads(jsonString)
        self.taskType.fromJson(
            jsonString=json.dumps(_from_json_dict['taskType'])
        )

    def isValid(self) -> bool:
        result : bool = super().isValid()
        return result

    def refreshProperties(self) -> NodeReturnValue:
        retValue = NodeReturnValue.OK

        if not self.isValid():
            retValue = NodeReturnValue.FAILURE
        else:
            # TODO: define properties
            pass

        return retValue
        

