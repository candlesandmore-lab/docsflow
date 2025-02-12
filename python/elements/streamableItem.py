

import json
from typing import Optional


class StreamableItem():
    def __init__(self):
        pass

    def __iter__(self):

        for key in self.__dict__:
            if isinstance(self.__getattribute__(key), StreamableItem):
                yield from self.__getattribute__(key)
            else:
                yield key, getattr(self, key)
    
    def toJson(self, indent : Optional[int] = None):
        __dict = dict(self)
        return json.dumps(__dict, indent=indent)
    
    def fromJson(  # noqa: F811
            self,
            jsonString : str
        ):
        pass
    

