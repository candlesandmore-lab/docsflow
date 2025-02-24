
from datetime import datetime
from enum import Enum
import json
from typing import Any, Optional

from python.data.dataFactory import DataFactory
from python.elements.baseNode import BaseNode, NodeReturnValue
from python.elements.datetimeItem import DatetimeItem
from python.elements.userItem import UserItem
from python.infra.jsonStuff import getFieldSave
from python.infra.timeStampMeta import utcDateTime

class NodeState(float, Enum):
    UNDEF = -1
    AVAILABLE = 0
    REVIEWED = 0.5
    CLOSED = 1

class NodeStateWeight(int, Enum):
    LOW = 1
    # 2,3
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 13



class BaseNodeWithState(BaseNode):
    def __init__(self, name:str, factory : DataFactory) -> None:
        super().__init__(name, factory)
        self.state : float = NodeState(NodeState.UNDEF)
        
         # uuid of child, weight
        self.childStateWeights : dict[str, NodeStateWeight] = {} # dict with "uuid" : weight

        # hook for status workers, place for status fields that are updated on demand and not stored in DB
        self.statusProperties : dict = {}  # key:value
        self.packIgnoreProperties.append('statusProperties')


    def getStatus(self, key, default) -> Any:
        return getFieldSave(self.statusProperties, key, default)
    
    def setStatus(self, key, value) -> None:
        self.statusProperties[key] = value

    def fromJson(
            self,
            jsonString : str
        ) -> None:
        super().fromJson(jsonString)
        
        _from_json_dict = json.loads(jsonString)
        self.state = NodeState(_from_json_dict['state'])

        # iterate over list of updates
        for childUUID in _from_json_dict['childStateWeights'].keys():
            self.childStateWeights[childUUID] = _from_json_dict['childStateWeights'][childUUID]



    def childByUUID(self, thisUUID : str) -> tuple[NodeReturnValue, BaseNode]:
        result : BaseNode
        retValue : NodeReturnValue = NodeReturnValue.FAILURE
        for child in self.childs :
            if child.uuid == thisUUID:
                result = child
                retValue = NodeReturnValue.OK
                break

        return retValue, result
    

    # state setting 
    #   update this node and its child status per META data and compare with roll up result, set the lower value
    def updateStateWithMetaData(self, path : str) -> tuple[bool, float]:
        success = True
        newState : float = NodeState(NodeState.UNDEF)

        for child in self.childs:
            childPath = str.join("/", [path, child.name])

            # iterate in tree
            if isinstance(child, BaseNodeWithState):
                child.updateStateWithMetaData(childPath)
            else:
                self.logger.error("Found node [{}] in tree which is not a status node, abort.".format(
                    childPath
                ))
                success = False
                break

        # update myself
        # what is meta-data (user input) saying?
        metaExists, metaDict = getFieldSave(self.properties, 'meta', None)
        metaState = NodeState.UNDEF

        if metaExists:
            fieldExists, metaStateList = getFieldSave(metaDict, 'state', None)
            if fieldExists:
                # get latest valid state entry
                latestUpdateTime = utcDateTime(datetime(2000, 1, 1)) # in the past
                latestStateDict : dict = {}
                fieldExists = False
                for stateDict in metaStateList:
                    if stateDict['targetDate'].when > latestUpdateTime:
                        latestUpdateTime = stateDict['targetDate'].when
                        latestStateDict = stateDict
                        fieldExists = True
            
            if fieldExists:
                # TODO: enum convertion from Meta data
                if latestStateDict['state'] == 'CLOSED':
                    metaState = NodeState.CLOSED
                elif latestStateDict['state'] == 'REVIEWED':
                    metaState = NodeState.REVIEWED
                elif latestStateDict['state'] == 'AVAILABLE':
                    metaState = NodeState.AVAILABLE

        if len(self.childs) == 0:
            # there is only META state or UNDEF, since node has no childs
            newState = metaState 
        else:
            # Roll up state of childs, compare to meta data and set this state accordingly
            rollUpSuccess, rollUpState = self.rolledUpState()
            if rollUpSuccess != NodeReturnValue.OK:
                newState = NodeState(NodeState.UNDEF)
                self.logger.error("Failure during state roll up, set state of node [{}] to [{}].".format(
                    path,
                    newState
                ))
            elif metaState == NodeState.UNDEF:
                # no user input, fully auto calculated
                newState = rollUpState
            elif rollUpState > metaState:
                self.logger.error("Failure during state roll up @ [{}], rolled up state [{}] is greater than meta-data set state [{}].".format(
                    path,
                    newState,
                    metaState
                ))
                # META wins, it is less and needs user attention
                newState = metaState
            elif rollUpState < metaState:
                # Roll-up wins, it is less and needs user attention
                self.logger.error("Failure during state roll up @ [{}], rolled up state [{}] is less than meta-data set state [{}].".format(
                    path,
                    newState,
                    metaState
                ))
                newState = rollUpState    
            else:
                # meta state and roll up say the same
                newState = metaState
            
        
        # Roll-up and Meta are the same
        self.logger.debug("Set state of [{}] to [{}].".format(
            path,
            newState
        ))
        self.state = newState

        return success, self.state
        
    # TODO: store state ID as enum in metadata
    def getStateDict(self, stateList : list, state : str) -> tuple[bool, dict]:
        foundIt : bool = False
        resultDict : dict = {}

        for stateEntry in stateList:
            # record with 'state' and 'targetDate' as DatetimeItem class
            if stateEntry['state'] == state:
                resultDict = stateEntry
                foundIt = True
                break

        return foundIt, resultDict

    def addOrUpdateChild(self, 
            child, 
            user : UserItem, 
            when : Optional[DatetimeItem] = None) -> None:

        super().addOrUpdateChild(child, user, when)

        # create association with weight
        statusKey = "{}".format(child.uuid)

        if statusKey not in self.childStateWeights.keys():
            self.childStateWeights[statusKey] = NodeStateWeight.CRITICAL # default is critical

    # status roll up
    def setChildStatusWeight(self, child : BaseNode, statusWeight : NodeStateWeight) -> NodeReturnValue:
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
            self.childStateWeights[statusKey] = statusWeight

        return retValue

    def rolledUpState(self) -> tuple[NodeReturnValue, float]:
        
        result : float
        retValue = NodeReturnValue.OK
        
        childsWeightedStatus : float = 0.0
        childsWeight : int = 0
        
        for statusKey in self.childStateWeights.keys():
            nReturnValue, child = self.childByUUID(statusKey)
            if nReturnValue != NodeReturnValue.OK:
                self.logger.error("Node [{}/{}] Failed to find child with UUID[{}].".format(
                    self.name,
                    self.nodeType,
                    self.uuid
                ))
                retValue = NodeReturnValue.FAILURE
                result = NodeState.UNDEF
                break
            else:
                if isinstance(child, BaseNodeWithState):
                    childNRetValue, childRolledUpStatus = child.rolledUpState()
                    if childNRetValue != NodeReturnValue.OK:
                        retValue = NodeReturnValue.FAILURE
                        break
                    else:
                        childsWeightedStatus = childsWeightedStatus + self.childStateWeights[statusKey] * childRolledUpStatus 
                        childsWeight = childsWeight + self.childStateWeights[statusKey]
                else:
                    self.logger.error("Node [{}/{}] has child with UUID[{}] which is not a StatusNode.".format(
                        self.name,
                        self.nodeType,
                        child.uuid
                    ))
                    retValue = NodeReturnValue.FAILURE
                    result = NodeState.UNDEF
                    break

        if retValue == NodeReturnValue.OK:
            if len(self.childStateWeights) == 0:
                # node itself must provide return value
                result = NodeState(self.state)
            else:
                result = childsWeightedStatus / float(childsWeight)

            if abs(result) > 1:
                retValue = NodeReturnValue.FAILURE
                self.logger.error("Node [{}/{}] has rolled up status out of boundaries [{}], should be in (-1,1).".format(
                            self.name,
                            self.nodeType,
                            result
                ))        

        #nRetValue, statusColor = self.statusAsColor(result)

        return retValue, result #, statusColor