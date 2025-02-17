
#
# allow to read user input via .docFlowMeta files in folder trees
#
import json
import os
from python.elements.datetimeItem import DatetimeItem
from python.infra.logging import getMainLogger
from python.infra.timeStampMeta import utcDateTimeFromIsoString


class MetaReaderJson():
    def __init__(self) -> None:
        self.logger = getMainLogger()

    def importFolderMetadata(
            self,
            folder : str
    ) -> tuple[bool, dict]:
        
        success = True
        metaTree : dict = {}
        
        if not os.path.isdir(folder):
            self.logger.error("Folder [{}] is not accessible.".format(
                folder
            ))
            success = False
        else:
            # files -> DOC
            for dirEntry in os.listdir(folder):
                fullDirEntryPath = os.path.join(folder, dirEntry)
                # test
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

    def __importItemMeta(self, contextMetaDict : dict) -> tuple[bool, dict]:
        result : dict = {}
        success = True

        if 'plan' in contextMetaDict.keys():
            success, result['plan'] = self.__importMetaStatusList(contextMetaDict['plan'])
        
        if success and 'status' in contextMetaDict.keys():
            success, result['status'] = self.__importMetaStatusList(contextMetaDict['status'])
        
        return success, result
    
    def __importMetaStatusList(self, metaStatusList : list) -> tuple[bool, list]:
        result : list = []
        success = True

        if not (metaStatusList, list):
            success = False
        else:
            for metaData in metaStatusList:
                targetState = metaData[0]
                targetDate = DatetimeItem(utcDateTimeFromIsoString(metaData[1]))
                    
                result.append(
                    {
                        'state':targetState,
                        'targetDate' : targetDate
                    }
                )

        return success, result