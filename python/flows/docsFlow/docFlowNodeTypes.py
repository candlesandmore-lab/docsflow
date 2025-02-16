import json
from python.elements.streamableItem import StreamableItem


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
        
        self.type = _from_json_dict['type']
        self.description = _from_json_dict['description']

class DocNodeType(DocFlowNodeType):
    def __init__(self, type : str = "UNDEF", description : str = ""):
        super().__init__(type, description)


class ContextNodeType(DocFlowNodeType):
    def __init__(self, type : str = "UNDEF", description : str = ""):
        super().__init__(type, description)
