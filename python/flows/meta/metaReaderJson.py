
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
            localMetaFilePath = "{}/.docFlowMeta.json".format(folder)
            if not os.path.exists(localMetaFilePath):
                # Need meta data file to map child context to context types
                self.logger.warning("Skip meta data search at [{}] due to missing .docFlowMetaData.json".format(
                    folder
                ))
            else:
                # read local meta data file first to understand child context
                with open(localMetaFilePath) as fileHandler:
                    # add context own tasks
                    contextMetaDict = json.load(fileHandler)
                    for itemKey in contextMetaDict:

                        success, metaTree[itemKey] = self.__importItemMeta(contextMetaDict[itemKey]) 
                        if not success:
                            self.logger.error("Cannot import meta data for [{}] from [{}].".format(
                                itemKey,
                                localMetaFilePath
                            ))


                # check hierarchical data
                for dirEntry in os.listdir(folder):
                    fullDirEntryPath = os.path.join(folder, dirEntry)
                    if os.path.isdir(fullDirEntryPath):
                        success, subDirMeta = self.importFolderMetadata(fullDirEntryPath)
                        # find the relevant meta data tree with same name property
                        if success:
                            foundMetaDataForSubDir = False
                            for nodeTypeKey in metaTree.keys():
                                fieldExists, dirnameWithLocalMetadata = getFieldSave(metaTree[nodeTypeKey], 'name', None)
                                if dirnameWithLocalMetadata == dirEntry:
                                    foundMetaDataForSubDir = True
                                    metaTree[nodeTypeKey].update(subDirMeta)
                            
                            if not foundMetaDataForSubDir:
                                success = False
                                self.logger.error("Found sub-dir [{}] with meta-data which is not mentioned in .docFlowMeta.json of its parent dir. Unable to import and map this data.".format(
                                    fullDirEntryPath
                                ))
                        
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