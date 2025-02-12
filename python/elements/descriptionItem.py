from python.elements.streamableItem import StreamableItem


class DescriptionItem(StreamableItem):
    def __init__(self, description : str):
        self.description = description
        
    # stream as datetime key : value
    def __flat_iter__(self) -> bool:
        return True