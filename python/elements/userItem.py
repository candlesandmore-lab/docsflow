from python.elements.streamableItem import StreamableItem


class UserItem(StreamableItem):
    def __init__(self, name : str, role : str):
        super().__init__()
        self.name : str = name
        self.role : str = role
