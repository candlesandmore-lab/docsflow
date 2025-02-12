from typing import List, Optional
from python.elements.datetimeItem import DatetimeItem
from python.elements.streamableItem import StreamableItem
from python.elements.updateItem import UpdateItem, UpdateType
from python.elements.userItem import UserItem
from python.infra.timeStampMeta import utcDateTime


class BaseNode(StreamableItem):
    def __init__(self):
        super().__init__()
        self.childs = List[BaseNode] = list()
        self.updates = List[UpdateItem] = list()

    def addChild(
            self, 
            child : BaseNode, 
            user : UserItem, 
            when : Optional[DatetimeItem] = None) -> None:
        if when is None:
            when = DatetimeItem(utcDateTime())

        self.updates.append(
            UpdateItem(
                kind=UpdateType.UPDATE,
                when=when,
                who=user,
                description="Add child node"
            )
        )
        pass

