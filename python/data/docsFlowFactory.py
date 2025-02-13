

# class that manages the translation between BL -and DB data structures

from enum import Enum
import json
from pymongo.collection import Collection

from python.data.mongoDBHandler import MongoDBHandler, mdbhReturnValue
from python.elements.baseNode import BaseNode, NodeType
from python.infra.logging import getMainLogger

class dffReturnValue(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    
class dffState(str, Enum):
    OK = "OK",
    NO_DB = "NO_DB"

# TODO: centralize list and access of collection names
dffCollections : list[str] = ["DocsFlowProjects"]

class DocsFlowFactory():
    def __init__(self, mongoDBHandler : MongoDBHandler, dbName : str = "DocsFlowDatabase"):
        self.logger = getMainLogger()
        self.mongoDBHandler = mongoDBHandler
        retValue, self.db = self.mongoDBHandler.getDB(
            dbName=dbName
        )
        if retValue != mdbhReturnValue.OK:
            self.state = dffState.NO_DB
            errMsg = "Cannot connect to MongoDB, factory is not functional."
            print(errMsg)
            self.logger.error(errMsg)
        else:
            self.state = dffState.OK
            self.logger.info("Connected to MongoDB:Database[{}]".format(dbName))

    def isFunctional(self):
        return self.state == dffState.OK

    def flushCaches(self) -> dffReturnValue:
        retValue = dffReturnValue.OK
        if not self.isFunctional():
            print("Cannot flush caches.")
        else:
            for collectionName in dffCollections:
                mdbhRetValue = self.mongoDBHandler.clearCache(self.db, collectionName)
                if mdbhRetValue != mdbhReturnValue.OK:
                    errMsg = "Failed to clear cache of collection [{}]. Abort."
                    print(errMsg)
                    self.logger.error(errMsg)
                    retValue = dffReturnValue.FAILURE
                    break
        return retValue

    # TODO: split/optimize storage per node type and store only DB ObjectId() references in specific collections
    def findCollection(self, nodeType : NodeType) -> tuple[dffReturnValue, Collection]:
        retValue = dffReturnValue.OK
        collectionName : str
        collection : Collection

        if not self.isFunctional():
            print("Not connected to a DB.")
            retValue = dffReturnValue.FAILURE
        else: 
            if nodeType == NodeType.PROJECT:
                collectionName = "DocsFlowProjects"
            elif nodeType == NodeType.DOC:
                retValue = dffReturnValue.FAILURE
            elif nodeType == NodeType.CONTEXT:
                retValue = dffReturnValue.FAILURE
            elif nodeType == NodeType.TASK:
                retValue = dffReturnValue.FAILURE

            if retValue == dffReturnValue.FAILURE:
                self.logger.error("Unable to identify collection name for node type [{}]".format(nodeType))
            else:
                mdbhRetValue, collection = self.mongoDBHandler.getCollection(
                    mongoDB=self.db,
                    collectionName=collectionName
                )
                if mdbhRetValue != mdbhReturnValue.OK:
                    retValue = dffReturnValue.FAILURE

        return retValue, collection        
    
    def insertNode(self, node : BaseNode) -> dffReturnValue:
        retValue = dffReturnValue.OK
        collection : Collection

        # insert into correct collection, based on node type
        retValue, collection = self.findCollection(node.nodeType)
        if retValue != dffReturnValue.OK:
            self.logger.error("Unable to identify DB collection to insert [{}] node into.".format(node.nodeType))
        else:
            nodeDict = dict(node)
            mdbhRetValue, insertResult = self.mongoDBHandler.insertDoc(
                mongoDBCollection=collection,
                docDict=nodeDict
            )
            if mdbhRetValue != mdbhReturnValue.OK:
                self.logger.error("Failed to insert [{}] node  ".format(node.nodeType))
                retValue = dffReturnValue.FAILURE

        return retValue
    
    # update or insert (if node does not exist yet)
    #   - search in correct collection based out BL UUID field of node
    def updateNode(self, node : BaseNode) -> dffReturnValue:
        retValue = dffReturnValue.OK
        collection : Collection

        # insert into correct collection, based on node type
        retValue, collection = self.findCollection(node.nodeType)
        if retValue != dffReturnValue.OK:
            self.logger.error("Unable to identify DB collection to update [{}] node into.".format(node.nodeType))
        else:
            nodeDict = dict(node)
            mdbhRetValue, insertResult = self.mongoDBHandler.replaceDoc(
                mongoDBCollection=collection,
                docDict=nodeDict,
                filter={ "uuid": nodeDict['uuid'] }
            )
            if mdbhRetValue != mdbhReturnValue.OK:
                self.logger.error("Failed to update [{}] node with uuid [{}] ".format(
                    node.nodeType,
                    nodeDict['uuid']
                ))
                retValue = dffReturnValue.FAILURE

        return retValue

    # db.student.aggregate([{ $project: { subject: 1, _id: 0 } }])
    def getAnyNodeProperties(self, nodeType : NodeType, propertyKeys : list[str]) -> tuple[dffReturnValue, list[str]]:
        result = []
        mdbhRetValuetValue, collection = self.findCollection(nodeType)
        dffRetValue = dffReturnValue.OK

        if mdbhRetValuetValue != dffReturnValue.OK:
            self.logger.error("Unable to identify DB collection to insert [{}] node into.".format(nodeType))
            dffRetValue = dffReturnValue.FAILURE
        else:
            projectionDict = {
                "_id": 1,
                "nodeType" : 1
            }
            for key in propertyKeys:
                projectionDict[key] = 1

            # { "$project" : { "nodeType": 1, "uuid" : 1, "_id": 1 } }
            pipeline = [
                { "$project" : projectionDict }
            ]
            Cursor = collection.aggregate(pipeline=pipeline)
            result = list(Cursor)

        return dffRetValue, result

    # get a node based on properties queried using getAnyNodeProperties()
    def getNode(self, listOfDocProperties : list[dict], index : int) -> tuple[dffReturnValue, BaseNode]:
        retValue = dffReturnValue.OK
        result : BaseNode
        if len(listOfDocProperties) < index:
            self.logger.error("Cannot select item #[{}] from list with lenght [{}]".format(
                index,
                len(listOfDocProperties)
            ))
            retValue = dffReturnValue.FAILURE
        else:
            nodeType = listOfDocProperties[index]['nodeType']
            mdbhRetValuetValue, collection = self.findCollection(nodeType)
            if mdbhRetValuetValue != dffReturnValue.OK:
                self.logger.error("Unable to identify DB collection to insert [{}] node into.".format(nodeType))
                retValue = dffReturnValue.FAILURE
            else:
                queryDict = { "_id": listOfDocProperties[index]['_id'] }
                mdbhRetValue, queryDoc, queryDocList = self.mongoDBHandler.getDoc(collection, queryDict)
                if len(queryDocList) != 1:
                    self.logger.error("Unable to handle number of returned nodes [{}]".format(len(queryDocList)))
                else:
                    # drop database '_id' field since it is not streamable (and not useful in BL layer)
                    nodeDict = queryDocList[0]
                    _ = nodeDict.pop("_id")  # of type ObjectId

                    result = BaseNode("", nodeType)
                    result.fromJson(
                        jsonString=json.dumps(nodeDict)
                    )

        return retValue, result

