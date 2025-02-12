

import json
from typing import Any, Generator, List, Optional

class StreamableItem():
    def __init__(self):
        pass

    # default: stream objects in hierarchy
    def __flat_iter__(self) -> bool:
        return False

    def __iter__(self) -> Generator[tuple[str, Any] | Any | tuple[str, list] | tuple[str, dict], Any, None]:

        for key in self.__dict__:
            # streaming requires some special handling for some objects
            if isinstance(self.__getattribute__(key), List):
                streamingDone : bool = False
                
                streamedList = []
                if len(self.__getattribute__(key)) == 0:
                    yield key, getattr(self, key)
                else:
                    for listEntry in self.__getattribute__(key):
                        if isinstance(listEntry, StreamableItem):
                            streamingDone = True
                            #print("Key = {} : Flat = {}".format(key, self.__getattribute__(key).__flat_iter__()))
                            if listEntry.__flat_iter__():
                                # do not build a hierarchy, just stream the objects fields
                                yield from listEntry
                            else:
                                fields = listEntry.__iter__()
                                dict = {}
                                for f in fields:
                                    dict[f[0]] = f[1]
                                streamedList.append(dict)
                        else:
                            yield key, getattr(self, key)

                if streamingDone:
                    yield key, streamedList
                    
            elif isinstance(self.__getattribute__(key), StreamableItem):
                streamingDone = True
                #print("Key = {} : Flat = {}".format(key, self.__getattribute__(key).__flat_iter__()))
                if self.__getattribute__(key).__flat_iter__():
                    # do not build a hierarchy, just stream the objects fields
                    yield from self.__getattribute__(key)
                else:
                    fields = self.__getattribute__(key).__iter__()
                    dict = {}
                    for f in fields:
                        dict[f[0]] = f[1]
                    yield key, dict
                    #self.__getattribute__(key).__iter__()

            else:
                yield key, getattr(self, key)
    
    def toJson(self, indent : Optional[int] = None):
        __dict = dict(self)
        return json.dumps(__dict, indent=indent)
    
    def fromJson(
            self,
            jsonString : str
        ) -> None :
        pass
    

