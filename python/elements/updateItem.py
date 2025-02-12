from enum import Enum
import json
from typing import Optional

from python.elements.datetimeItem import DatetimeItem
from python.elements.descriptionItem import DescriptionItem
from python.elements.streamableItem import StreamableItem
from python.elements.userItem import UserItem
from python.infra.timeStampMeta import utcDateTimeFromIsoString

class UpdateType(int, Enum):
    CREATE = 0
    UPDATE = 1
    DELETE = 2
    UNDEF = 3
        
    def __repr__(self): 
        return "{}".format(self.value)
        
class UpdateItem(StreamableItem):
    # create by user, flow or BL
    def __init__(
            self, 
            when : Optional[DatetimeItem] = None, 
            who : Optional[UserItem] = None, 
            description : Optional[DescriptionItem] = None,
            kind : Optional[UpdateType] = UpdateType.UNDEF
        ):
        self.when = when
        self.who = who
        self.description = description
        self.kind = kind

    # restore from JSON into BL format
    def fromJson(
            self,
            jsonString : str
        ) -> None :
        _from_json_dict = json.loads(jsonString)
        
        self.when = DatetimeItem(utcDateTimeFromIsoString(_from_json_dict['when']))
        self.who = _from_json_dict['who']
        self.description = _from_json_dict['description']
        self.kind = _from_json_dict['kind']
