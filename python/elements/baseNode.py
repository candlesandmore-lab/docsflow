from enum import Enum
import json
from typing import List, Optional, Any
import uuid
from python.elements.datetimeItem import DatetimeItem
from python.elements.descriptionItem import DescriptionItem
from python.elements.streamableItem import StreamableItem
from python.elements.updateItem import UpdateItem, UpdateType
from python.elements.userItem import UserItem
from python.infra.logging import getMainLogger
from python.infra.timeStampMeta import utcDateTime

class NodeType(str, Enum):
    PROJECT = "PROJECT"
    CONTEXT = "CONTEXT"
    DOC = "DOC"
    TASK = "TASK"
        
    def __repr__(self): 
        return "{}".format(self.value)

class NodeReturnValue(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    
class BaseNode(StreamableItem):
    def __init__(self, name : str, nodeType : NodeType) -> None:
        super().__init__()
        self.logger = getMainLogger()
        self.packIgnoreProperties.append("logger")

        self.name = name
        self.nodeType : NodeType = nodeType
        self.uuid : str = "{}".format(uuid.uuid4())  # later DB IDs
        self.childs : List[BaseNode] = list()
        self.updates : List[UpdateItem] = list()
        self.testIntList = [1, 43, 5]
        self.properties : dict = {
            "foo" : "bar"
        }

    def isValid(self) -> bool:
        if self.name == "":
            self.logger.error("Node is missing name property.")

        return self.name != ""
    
    def refreshProperties(self) -> NodeReturnValue:
        return NodeReturnValue.OK

    def addOrUpdateChild(
            self, 
            child, 
            user : UserItem, 
            when : Optional[DatetimeItem] = None) -> None:
        
        if when is None:
            when = DatetimeItem(utcDateTime())

        
        # add or update
        operation : str = "create"
        for existingChild in self.childs:
            if child.uuid == existingChild.uuid:
                operation = "update"

        if operation == "update":
            existingChild = child
        else:
            self.childs.append(child)

        update = UpdateItem(
            kind=UpdateType.UPDATE,
            when = when,
            who=user,
            description=DescriptionItem("[{}] child [{}]/[{}].".format(
                operation,
                child.nodeType,
                child.name
            ))
        )
        
        self.updates.append(
            update    
        )

    # restore from JSON into BL format
    def fromJson(
            self,
            jsonString : str
        ) -> None:
        _from_json_dict = json.loads(jsonString)
        
        self.name = _from_json_dict['name']
        self.uuid = _from_json_dict['uuid']
        self.nodeType = NodeType[_from_json_dict['nodeType']]
        self.testIntList = _from_json_dict['testIntList']
        
        # iterate over tree
        for childDict in _from_json_dict['childs']:
            childNode = BaseNode("", childDict['nodeType'])
            childNode.fromJson(
                jsonString=json.dumps(childDict)
            )
            self.childs.append(childNode)

        # iterate over list of updates
        for updateDict in _from_json_dict['updates']:
            updateNode = UpdateItem()
            updateNode.fromJson(
                jsonString=json.dumps(updateDict)
            )
            self.updates.append(updateNode)
            
        # take properties, all simple for now
        self.properties = _from_json_dict['properties']

    def updateProperties(
            self, 
            propDict : dict,
            user : UserItem) -> None:
        for key in propDict.keys():
            self.updateProperty(key, propDict[key], user)

    def updateProperty(
            self, 
            key : str, 
            value : Any,
            user : UserItem) -> None:
        updMsg = "User [{}] updated project [{}] property [{}] to [{}].".format(
            user.toDict(),
            self.name,
            key,
            value
        )
        self.properties[key] = value
        
        update = UpdateItem(
                kind=UpdateType.UPDATE,
                when = DatetimeItem(utcDateTime()),
                who=user,
                description=DescriptionItem(updMsg)
            )
        self.logger.info(updMsg)
        
        self.updates.append(
            update    
        )
                
