
# #user interface for users that edit json file -> none, just for testing
import json
from python.data.docFlowNodeFactory import DocFlowNodeFactory
from python.elements.baseNode import BaseNode
from python.elements.streamableItem import StreamableDict
from python.elements.userItem import UserItem
from python.flows.docsFlow.projectNode import ProjectNode
from python.flows.meta.metaReaderJson import MetaReaderJson
from python.infra.logging import getMainLogger


class ProjectJsonUI():
    def __init__(
            self,
            user : UserItem,
            docNodeFactory : DocFlowNodeFactory,
            project :  ProjectNode,
            metaDir : str):
        
        self.logger = getMainLogger()

        self.user = user
        self.docNodeFactory = docNodeFactory
        self.project = project
        self.metaDir = metaDir

        self.importMetaData()
        self.mergeMetaData()
    
    #
    # - match metadata by name, which should work for
    #   -  files and folders that match there name to a meta data dictionary name field
    # IFF there is no match, we have meta-data for file/folders that do not exist yet and for which the name is not defined yet
    #   - this should not happen in a proper UI
    #   - it is a flaw of the disk based UI
    def mergeMetaData(self):
        mergedMeta = self.mergeContextMetaData(self.project, self.metaFromDir, ".")
        if not mergedMeta:
            self.logger.warning("Unable to merge any meta-data into the project tree.")
            
    def mergeContextMetaData(self, node : BaseNode, metaDict : StreamableDict, hier : str) -> bool:
        mergedData = False

        # this nodes meta data that is found
        propertyMetaDict = StreamableDict()
        propertyMetaDict['meta'] = StreamableDict()

        for metaKey in metaDict.keys():
            # key is part of list ContextType or DocType (see constants.py)
            if not isinstance(metaDict[metaKey], dict):
                #  for now, just add the plan and status
                propertyMetaDict['meta'][metaKey] = metaDict[metaKey]
            else:
                if 'name' not in metaDict[metaKey].keys():
                    # cannot match
                    self.logger.warning("JSON UI cannot match meta data [{}] due to missing name property.".format(
                        str.join("/", [hier, metaKey])
                    ))
                else:
                    childName = metaDict[metaKey]['name']
            
                    childExist, child = self.docNodeFactory.getChildNodeByName(
                        parent=node,
                        name=childName
                    )
                    if not childExist:
                        self.logger.warning("JSON UI cannot import meta data for nodes [{}] that do not exist.".format(
                            str.join("/", [hier, metaKey, childName])
                        ))
                    else:
                        # now we got a PROJ or CONTEXT with name matching
                        mergedData = self.mergeContextMetaData(
                            node=child,
                            metaDict=metaDict[metaKey],
                            hier=str.join("/", [hier, metaKey, childName])
                        )

        # Update with any meta data found for this node itself
        node.updateProperties(
            propertyMetaDict,
            user=self.user
        )

        return mergedData

    def importMetaData(self):
        self.metaReader = MetaReaderJson()
        success, self.metaFromDir = self.metaReader.importFolderMetadata(
            folder=self.metaDir
        )
        
        if not success:
            self.logger.error("Error whilst creating UI.")