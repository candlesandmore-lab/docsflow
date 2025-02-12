from python.elements.streamableItem import StreamableItem


class UserItem(StreamableItem):
    def __init__(self, name : str, role : str):
        self.name : str = name
        self.role : str = role
