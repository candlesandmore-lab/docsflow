
import os
from python.elements.baseNode import BaseNode, NodeReturnValue, NodeType
from python.elements.datetimeItem import DatetimeItem
from python.elements.userItem import UserItem
from python.flows.docsFlow.docNode import DocNode
from python.infra.timeStampMeta import utcDateTimeFromEpochSeconds

#
# we have two context nodes:
#  (a) those which are a container for task, not related to any folder on disk (e.g. container for tasks)
#  (b) those which are represented by a folder on disk
#
class ContextNode(BaseNode):
    def __init__(self, name:str, nodeType:NodeType):
        super().__init__(name, nodeType)
        
    def isValid(self) -> bool:
        result : bool = super().isValid()
        if result:
            # type (b)
            if 'contextPath' in self.properties.keys():
                if not os.path.isdir(self.properties['contextPath']):
                    result = False
                    self.logger.error("Context [{}] is associated to disk folder [{}] which does not exist.".format(
                        self.name,
                        self.properties['docPath']
                    ))

        return result
    
    def setContextPath(self, path : str) -> None:
        self.properties['contextPath'] = path

    def refreshProperties(self) -> NodeReturnValue:
        retValue = NodeReturnValue.OK

        if not self.isValid():
            retValue = NodeReturnValue.FAILURE
            self.logger.error("Context [{}] is not valid.".format(self.name))
        else:
            stats = os.stat(self.properties['contextPath'])
            self.properties['size'] = stats.st_size
            self.properties['owner'] = stats.st_uid
            self.properties['size'] = stats.st_size
            self.properties['mupdateTime'] = DatetimeItem(
                when=utcDateTimeFromEpochSeconds(os.path.getmtime(self.properties['contextPath']))
            )
            self.properties['createTime'] = DatetimeItem(
                when=utcDateTimeFromEpochSeconds(os.path.getctime(self.properties['contextPath']))
            )

        return retValue
        

    def importFolderContent(
            self,
            folder : str,
            user : UserItem
    ) -> NodeReturnValue:
        
        retValue = NodeReturnValue.OK
        
        self.setContextPath(folder)
        
        if not self.isValid():
            retValue = NodeReturnValue.FAILURE
        else:
            # files -> DOC
            for dirEntry in os.listdir(self.properties['contextPath']):
                fullDirEntryPath = os.path.join(self.properties['contextPath'], dirEntry)
                if os.path.isfile(fullDirEntryPath):

                    newDocNode = DocNode(
                        name = dirEntry,
                        nodeType=NodeType.DOC
                    )
                    newDocNode.setDocPath(fullDirEntryPath)
                    newDocNode.refreshProperties()
                    self.addOrUpdateChild(
                        child=newDocNode,
                        user=user)

                # folder -> CONTEXT with folder association
                elif os.path.isdir(fullDirEntryPath):
                    newContextNode = ContextNode(
                        name=dirEntry,
                        nodeType=NodeType.CONTEXT
                    )
                    newContextNode.setContextPath(fullDirEntryPath)
                    newContextNode.refreshProperties()
                    self.addOrUpdateChild(
                        child=newContextNode,
                        user=user)

                    # iterate into folder tree
                    newContextNode.importFolderContent(
                        folder=fullDirEntryPath,
                        user=user
                    )
                else:
                    self.logger.info("Ignore folder content [{}], it is not a file or folder in [{}].".format(
                        dirEntry,
                        fullDirEntryPath
                    ))
        return retValue