

import json
from typing import List, Optional


class StreamableItem():
    def __init__(self) -> None:
        # packing support with class internal properties that shall be ignored
        self.packIgnoreProperties : list[str] = ["packIgnoreProperties"]

    def toDict(self) -> dict:
        resultDict = {}

        for key in self.__dict__:
            if key not in self.packIgnoreProperties:
                
                if isinstance(self.__getattribute__(key), List):
                    if len( self.__getattribute__(key)) == 0:
                        resultDict[key] = self.__getattribute__(key)
                    else:
                        # support list of StreamableItem or base type, no arbitrary objects
                        if isinstance(self.__getattribute__(key)[0], StreamableItem):
                            resultDict[key] = [item.toDict() for item in self.__getattribute__(key)]
                        else:
                            resultDict[key] = self.__getattribute__(key)
                    
                elif isinstance(self.__getattribute__(key), dict):
                    resultDict[key] = {}
                    for dictKey in self.__getattribute__(key).keys():
                        if isinstance(self.__getattribute__(key)[dictKey], StreamableItem):
                            resultDict[key][dictKey] = self.__getattribute__(key)[dictKey].toDict()
                        else:
                            resultDict[key][dictKey] = self.__getattribute__(key)[dictKey]

                else:
                    if isinstance(self.__getattribute__(key), StreamableItem):
                        resultDict[key] = self.__getattribute__(key).toDict()
                    else:
                        resultDict[key] = self.__getattribute__(key)
    
        return resultDict                    
    
    def toJson(self, indent : Optional[int] = None):
        __dict = self.toDict()
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
