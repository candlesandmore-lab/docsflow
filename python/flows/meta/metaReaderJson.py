
#
# allow to read user input via .docFlowMeta files in folder trees
#
import json
import os
from python.elements.datetimeItem import DatetimeItem
from python.elements.streamableItem import StreamableDict, StreamableItem, StreamableList
from python.flows.docsFlow.docFlowNodeTypes import DocFlowNodeType
from python.infra.jsonStuff import getFieldSave, updateFieldIfValueNotNone
from python.infra.logging import getMainLogger
from python.infra.timeStampMeta import utcDateTimeFromIsoString


class MetaReaderJson(StreamableItem):
    def __init__(self) -> None:
        super().__init__()
        self.logger = getMainLogger()
        self.packIgnoreProperties.append("logger")

    def importFolderMetadata(
            self,
            folder : str
    ) -> tuple[bool, StreamableDict]:
        
        success = True
        metaTree = StreamableDict()

        if not os.path.isdir(folder):
            self.logger.error("Folder [{}] is not accessible.".format(
                folder
            ))
            success = False
        else:
            # files -> DOC
            for dirEntry in os.listdir(folder):
                fullDirEntryPath = os.path.join(folder, dirEntry)
                # TODO: handle context to directory aliasing
                #            itemKey == context, includes field 'alias' with dirpath from here on.
                if dirEntry == ".docFlowMeta.json" and os.path.isfile(fullDirEntryPath):
                    with open(fullDirEntryPath) as fileHandler:
                        # add context own tasks
                        contextMetaDict = json.load(fileHandler)
                        for itemKey in contextMetaDict:
                            success, metaTree[itemKey] = self.__importItemMeta(contextMetaDict[itemKey])
                            if not success:
                                self.logger.error("Cannot import meta data for [{}] from [{}].".format(
                                    itemKey,
                                    fullDirEntryPath
                                ))
                                break
                                                            
                # folder -> CONTEXT with folder association
                elif os.path.isdir(fullDirEntryPath):
                    success, metaTree[dirEntry] = self.importFolderMetadata(fullDirEntryPath)
                    if not success:
                        break

        return success, metaTree

    def __importItemMeta(self, contextMetaDict : dict) -> tuple[bool, StreamableDict]:
        result = StreamableDict()
        success = True

        if 'plan' in contextMetaDict.keys():
            success, result['plan'] = self.__importMetaStatusList(contextMetaDict['plan'])
        
        if success and 'status' in contextMetaDict.keys():
            success, result['status'] = self.__importMetaStatusList(contextMetaDict['status'])

        # node meta properties
        nodeTypeInfo = DocFlowNodeType()
        nodeTypeInfo.fromDict(contextMetaDict)
        result['nodeType'] = nodeTypeInfo

        fieldExists, metaName = getFieldSave(contextMetaDict, 'name', None)
        updateFieldIfValueNotNone(result, 'name', metaName)
        
        return success, result
    
    def __importMetaStatusList(self, metaStatusList : list) -> tuple[bool, StreamableList]:
        result = StreamableList()
        success = True

        if not (metaStatusList, list):
            success = False
        else:
            for metaData in metaStatusList:
                streamableDict = StreamableDict() 

                streamableDict['state'] = metaData[0]
                streamableDict['targetDate'] = DatetimeItem(utcDateTimeFromIsoString(metaData[1]))
                 
                result.append(
                   streamableDict
                )

        return success, result