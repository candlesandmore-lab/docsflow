
from enum import Enum
import json
from typing import Optional

from python.data.dataFactory import DataFactory
from python.elements.baseNode import BaseNode, NodeReturnValue
from python.elements.datetimeItem import DatetimeItem
from python.elements.userItem import UserItem


class NodeStatus(float, Enum):
    UNDEF = -1

class NodeStatusWeight(int, Enum):
    LOW = 1
    # 2,3
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 13

class BaseNodeWithStatus(BaseNode):
    def __init__(self, name:str, factory : DataFactory) -> None:
        super().__init__(name, factory)
        self.status : float = NodeStatus(NodeStatus.UNDEF)
         # uuid of child, weight
        self.childStatusWeights : dict[str, NodeStatusWeight] = {} # dict with "uuid" : weight


    def fromJson(
            self,
            jsonString : str
        ) -> None:
        super().fromJson(jsonString)
        
        _from_json_dict = json.loads(jsonString)
        self.status = NodeStatus(_from_json_dict['status'])

        # iterate over list of updates
        for childUUID in _from_json_dict['childStatusWeights'].keys():
            self.childStatusWeights[childUUID] = _from_json_dict['childStatusWeights'][childUUID]


    def childByUUID(self, thisUUID : str) -> tuple[NodeReturnValue, BaseNode]:
        result : BaseNode
        retValue : NodeReturnValue = NodeReturnValue.FAILURE
        for child in self.childs :
            if child.uuid == thisUUID:
                result = child
                retValue = NodeReturnValue.OK
                break

        return retValue, result
    
    def addOrUpdateChild(self, 
            child, 
            user : UserItem, 
            when : Optional[DatetimeItem] = None) -> None:

        super().addOrUpdateChild(child, user, when)

        # create association with weight
        statusKey = "{}".format(child.uuid)

        if statusKey not in self.childStatusWeights.keys():
            self.childStatusWeights[statusKey] = NodeStatusWeight.CRITICAL # default is critical


    def setChildStatusWeight(self, child : BaseNode, statusWeight : NodeStatusWeight) -> NodeReturnValue:
        retValue = NodeReturnValue.OK
        nReturnValue, myChild = self.childByUUID(child.uuid)
        if nReturnValue != NodeReturnValue.OK:
            self.logger.error("Node [{}/{}] Failed to find child with UUID[{}].".format(
                self.name,
                self.nodeType,
                child.uuid
            ))
            retValue = NodeReturnValue.FAILURE
        else:
            statusKey = "{}".format(child.uuid)
            self.childStatusWeights[statusKey] = statusWeight

        return retValue

    def rolledUpStatus(self) -> tuple[NodeReturnValue, float]:
        
        result : float = NodeStatus(NodeStatus.UNDEF)
        retValue = NodeReturnValue.OK
        
        childsWeightedStatus : float = 0.0
        childsWeight : int = 1
        
        for statusKey in self.childStatusWeights.keys():
            nReturnValue, child = self.childByUUID(statusKey)
            if nReturnValue != NodeReturnValue.OK:
                self.logger.error("Node [{}/{}] Failed to find child with UUID[{}].".format(
                    self.name,
                    self.nodeType,
                    self.uuid
                ))
                retValue = NodeReturnValue.FAILURE
                result = NodeStatus.UNDEF
                break
            else:
                if isinstance(child, BaseNodeWithStatus):
                    childsWeightedStatus = childsWeightedStatus + self.childStatusWeights[statusKey] *  child.status
                    childsWeight = childsWeight + self.childStatusWeights[statusKey]
                else:
                    self.logger.error("Node [{}/{}] has child with UUID[{}] which is not a StatusNode.".format(
                        self.name,
                        self.nodeType,
                        child.uuid
                    ))
                    retValue = NodeReturnValue.FAILURE
                    result = NodeStatus.UNDEF
                    break

        if retValue == NodeReturnValue.OK:
            if len(self.childStatusWeights) == 0:
                # node itself must provide return value
                result = NodeStatus(NodeStatus.UNDEF)
            else:
                result = childsWeightedStatus / float(childsWeight)

        return retValue, result
