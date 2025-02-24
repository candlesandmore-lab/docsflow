
import json
import os
from python.data.dataFactory import DataFactory
from python.elements.baseNode import NodeReturnValue, NodeType
from python.elements.datetimeItem import DatetimeItem
from python.elements.userItem import UserItem
from python.flows.docsFlow.docFlowNodeTypes import ContextNodeType
from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.infra.timeStampMeta import utcDateTimeFromEpochSeconds

#
# we have two context nodes:
#  (a) those which are a container for task, not related to any folder on disk (e.g. container for tasks)
#  (b) those which are represented by a folder on disk
#

class ContextNode(BaseNodeWithState):
    def __init__(self, name:str, factory : DataFactory):
        super().__init__(
            name=name, 
            factory=factory)
        
        self.contextType = ContextNodeType()
        # TODO: set default values for properties, such that stepwise constructed nodes have all props

    def fromJson(
            self,
            jsonString : str
        ) -> None:
        super().fromJson(jsonString)

        _from_json_dict = json.loads(jsonString)
        self.contextType.fromJson(
            jsonString=json.dumps(_from_json_dict['contextType'])
        )
     
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

    # CONSTRUCTION
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
        
    # TODO: provide ignore file pattern, to streamline e.g. JSON meta data flow. We don't want this file in BL data
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
            # TODO: handle context to directory aliasing, read from .docFlowMeta.json
            #            itemKey == context, includes field 'alias' with dirpath from here on.
            # files -> DOC
            for dirEntry in os.listdir(self.properties['contextPath']):
                fullDirEntryPath = os.path.join(self.properties['contextPath'], dirEntry)
                if os.path.isfile(fullDirEntryPath):

                    newDocNode = self.factory.constructNode(NodeType.DOC)
                    newDocNode.name = dirEntry

                    newDocNode.setDocPath(fullDirEntryPath)
                    newDocNode.refreshProperties()
                    self.addOrUpdateChild(
                        child=newDocNode,
                        user=user)

                # folder -> CONTEXT with folder association
                elif os.path.isdir(fullDirEntryPath):
                    newContextNode = self.factory.constructNode(NodeType.CONTEXT)
                    newContextNode.name = dirEntry
                    
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