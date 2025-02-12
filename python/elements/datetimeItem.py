from datetime import datetime

from python.elements.streamableItem import StreamableItem


class DatetimeItem(StreamableItem):
    def __init__(self, when : datetime):
        self.when = when

    def __iter__(self): 
        # This allows iteration over the keys of the dictionary 
        yield 'when', self.when.isoformat()

    def __getitem__(self, key): 
        # This allows access to the values using the keys 
        if key == 'when': 
            return self.when.isoformat() 
        else: 
            raise KeyError(f"{key} not found") 
 
    def __repr__(self): 
        # For a nice representation of the object 
        return "DD{}".format(
            self.when.isoformat()
        )
