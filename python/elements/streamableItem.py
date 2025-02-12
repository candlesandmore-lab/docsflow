import json


class StreamableItem:
    def __init__(self):
        pass


    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)
    
    def streamJson(self):
        return dict(self)
        #return json.dumps(self.__dict__)
        '''
        result = {}
        attributeNames = self.packedAttributeNames()

        for attributeName in attributeNames:
            try:
                attributeValue = getattr(self, attributeName)
                if isinstance(attribute, int):
                    result[attributeName] : attributeName
            except Exception as err:
                errMsg = "Fatal issue whilst reading attribute [{}] for streaming - [{}].".format(
                    attributeName,
                    err
                )
        '''
        