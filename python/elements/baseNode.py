from typing import List, Optional
import uuid
from python.elements.datetimeItem import DatetimeItem
from python.elements.descriptionItem import DescriptionItem
from python.elements.streamableItem import StreamableItem
from python.elements.updateItem import UpdateItem, UpdateType
from python.elements.userItem import UserItem
from python.infra.timeStampMeta import utcDateTime


class BaseNode(StreamableItem):
    def __init__(self) -> None:
        super().__init__()
        self.uuid : uuid.UUID = uuid.uuid4()  # later DB IDs
        self.childs : List[BaseNode] = list()
        self.updates : List[UpdateItem] = list()
        self.lastUpdate : UpdateItem = None
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

        self.lastUpdate = update 
        

