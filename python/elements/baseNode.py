from enum import Enum
import json
from typing import List, Optional
import uuid
from python.elements.datetimeItem import DatetimeItem
from python.elements.descriptionItem import DescriptionItem
from python.elements.streamableItem import StreamableItem
from python.elements.updateItem import UpdateItem, UpdateType
from python.elements.userItem import UserItem
from python.infra.timeStampMeta import utcDateTime

class NodeType(int, Enum):
    PROJECT = 0
    CONTEXT = 1
    DOC = 2
    TASK = 3
        
    def __repr__(self): 
        return "{}".format(self.value)

class BaseNode(StreamableItem):
    def __init__(self, name : str, nodeType : NodeType) -> None:
        super().__init__()
        self.name = name
        self.nodeType : NodeType = nodeType
        self.uuid : str = "{}".format(uuid.uuid4())  # later DB IDs
        self.childs : List[BaseNode] = list()
        self.updates : List[UpdateItem] = list()
        self.testIntList = [1, 43, 5]

    def addChild(
            self, 
            child, 
            user : UserItem, 
            when : Optional[DatetimeItem] = None) -> None:
        
        if when is None:
            when = DatetimeItem(utcDateTime())

        update = UpdateItem(
                kind=UpdateType.UPDATE,
                when = when,
                who=user,
                description=DescriptionItem("Added child ...")
            )
        
        self.updates.append(
            update    
        )

        self.childs.append(child)

        
    # restore from JSON into BL format
    def fromJson(
            self,
            jsonString : str
        ) -> None:
        _from_json_dict = json.loads(jsonString)
        
        self.name = _from_json_dict['name']
        self.uuid = _from_json_dict['uuid']
        self.nodeType = _from_json_dict['nodeType']
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


