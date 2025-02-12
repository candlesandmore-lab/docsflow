from datetime import datetime
from enum import Enum

from python.elements.datetimeItem import DatetimeItem
from python.elements.descriptionItem import DescriptionItem
from python.elements.streamableItem import StreamableItem
from python.elements.userItem import UserItem

class UpdateType(str, Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
        
class UpdateItem(StreamableItem):
    def __init__(
            self, 
            when : DatetimeItem, 
            who : UserItem, 
            description : DescriptionItem,
            kind : UpdateType = UpdateType.UPDATE
            ):
        self.when = when
        self.who = who
        self.description = description
        self.kind = kind

    # customer streaming
    '''
    def __getitem__(self, key): 
        print(key)
        # This allows access to the values using the keys 
        if key == 'kind': 
            return UpdateType[self.kind].value
        else: 
            return super().__getitem__(key)
    '''