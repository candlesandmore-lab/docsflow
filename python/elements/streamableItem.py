

import json
from typing import Any, Generator, List, Optional


class StreamableItem():
    def __init__(self) -> None:
        # packing support with class internal properties that shall be ignored
        self.packIgnoreProperties : list[str] = ["packIgnoreProperties"]

    # default: stream objects in hierarchy
    def __flat_iter__(self) -> bool:
        return False

    def __iter__(self) -> Generator[tuple[str, Any] | Any | tuple[str, list] | tuple[str, dict], Any, None]:


        for key in self.__dict__:
            if key not in self.packIgnoreProperties:
                #if isinstance(self.__getattribute__(key), DatetimeItem):
                #    yield key, self.__getattribute__(key).isoformat()
                # streaming requires some special handling for some objects
                #  (a) list of entities, like UpdateItem
                if isinstance(self.__getattribute__(key), List):
                    streamingDone : bool = False
                    
                    streamedList = []
                    if len(self.__getattribute__(key)) == 0:
                        yield key, getattr(self, key)
                    else:
                        for listEntry in self.__getattribute__(key):
                            if isinstance(listEntry, StreamableItem):
                                # e.g. UpdateItem is such StreamableItem
                                streamingDone = True
                                #print("Key = {} : Flat = {}".format(key, self.__getattribute__(key).__flat_iter__()))
                                if listEntry.__flat_iter__():
                                    # do not build a hierarchy, just stream the objects fields
                                    yield from listEntry
                                else:
                                    fields = listEntry.__iter__()
                                    listEntryDict = {}
                                    for f in fields:
                                        listEntryDict[f[0]] = f[1]
                                    streamedList.append(listEntryDict)
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
                        propertyDict = {}
                        for f in fields:
                            propertyDict[f[0]] = f[1]
                        yield key, propertyDict
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
    


'''
# ++++ TODO ++++ FIX this stuff, to stream properties with timestamps
elif isinstance(self.__getattribute__(key), dict):
    streamedDict = {}
    for dictKey in self.__getattribute__(key).keys():
        if dictKey == "mupdateTime":
            print("FOO#1")
        dictEntry = self.__getattribute__(key)[dictKey]
        if isinstance(dictEntry, StreamableItem):
            #print("Key = {} : Flat = {}".format(key, self.__getattribute__(key).__flat_iter__()))
            if dictEntry.__flat_iter__():
                # do not build a hierarchy, just stream the objects fields
                yield from dictEntry
            else:
                fields = dictEntry.__iter__()
                for f in fields:
                    streamedDict[f[0]] = f[1]
        else:
            streamedDict[dictKey] = getattr(self.__getattribute__(key), dictKey)

    yield key, streamedDict
'''
