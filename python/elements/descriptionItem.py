from python.elements.streamableItem import StreamableItem


class DescriptionItem(StreamableItem):
    def __init__(self, description : str):
        self.description = description
        