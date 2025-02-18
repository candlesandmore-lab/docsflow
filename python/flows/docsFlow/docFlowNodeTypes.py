import json
from python.elements.streamableItem import StreamableItem
from python.infra.jsonStuff import getFieldSave


class DocFlowNodeType(StreamableItem):
    def __init__(self, type : str = "UNDEF", description : str = ""):
        super().__init__()
        self.type : str = type
        self.description : str = description

    def fromJson(
            self,
            jsonString : str
        ) -> None :
        
        _from_json_dict = json.loads(jsonString)

        self.fromDict(_from_json_dict)

    def fromDict(
            self,
            _from_json_dict : dict
        ) -> None :

        overwrite, self.type = getFieldSave(_from_json_dict, 'type', self.type)
        overwrite, self.description = getFieldSave(_from_json_dict, 'description', self.description)
        
class DocNodeType(DocFlowNodeType):
    def __init__(self, type : str = "UNDEF", description : str = ""):
        super().__init__(type, description)


class ContextNodeType(DocFlowNodeType):
    def __init__(self, type : str = "UNDEF", description : str = ""):
        super().__init__(type, description)

class TaskNodeType(DocFlowNodeType):
    def __init__(self, type : str = "UNDEF", description : str = ""):
        super().__init__(type, description)