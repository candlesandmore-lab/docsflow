
'''
Base node of a project tree, includes basic operations that are shared by all specialized nodes
'''

from python.elements.streamableItem import StreamableItem


class BaseElement(StreamableItem):
    def __init__(self):
        self.createdDateTime = None
        self.updates
        pass


        