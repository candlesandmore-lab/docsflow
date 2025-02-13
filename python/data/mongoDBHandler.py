
# interface between BL and DB
from enum import Enum
from typing import Any, Iterable, Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult
from bson.raw_bson import RawBSONDocument

from python.infra.logging import getMainLogger

class mdbhReturnValue(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    CLIENT_FAILURE = "CLIENT_FAILURE"

    
class MongoDBHandler():

    def __init__(
            self,
            host : Optional[str] = "localhost",
            port : Optional[int] = 27017,
            replicaSet : Optional[Any] = None):
        
        self.logger = getMainLogger()
        # dbLocation=some-host:port
        self.host = host
        self.port = port
        self.replicaSet = replicaSet
        self.mongoDBClient : MongoClient

        if replicaSet is None:
            # e.g. mongodb://localhost:27017/"
            self.mongoDBClient = MongoClient("mongodb://{}:{}/".format(host, port), 
                serverSelectionTimeoutMS = 2000, 
                tz_aware=True)
        else:
            self.mongoDBClient = MongoClient("mongodb://{}:{}/".format(host, port), 
                serverSelectionTimeoutMS = 2000, 
                tz_aware=True,
                replicaSet=replicaSet)

        try:
            self.serverInfo = self.mongoDBClient.server_info() # will throw an exception
            self.logger.info("Connected successfully to [{}]".format(self.serverInfo))
        except BaseException  as Error:
            errMsg = "Fatal whilst initializing MongoDB conection - could not connect to server: {}:{} {}".format(host, port, Error)
            print("*ERR* : [{}]".format(errMsg))
            self.logger.error(errMsg)

    def isFunctional(self) -> bool:
        if self.mongoDBClient is not None:
            return True
        else:
            return False

    def getDB(self, dbName : str) -> tuple[mdbhReturnValue, Database] :
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        mongoDB : Database
        
        if not self.isFunctional():
            self.logger.error("DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                mongoDB   = self.mongoDBClient[dbName]
                self.logger.debug("Connected to DB [{}].".format(dbName))
            except BaseException as Error:
                errMsg = "Could not get/create database: {} {}".format(dbName, Error)
                print(errMsg)
                self.logger.error(errMsg)
                retValue = mdbhReturnValue.FAILURE

        return retValue, mongoDB

    def createCollection(self, mongoDB:Database, collectionName:str, schemaTimeseriesMeta=None) -> tuple[mdbhReturnValue, Collection]:
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        mongoDBCollection : Collection

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                retValue, mongoDBCollection = self.getCollection(mongoDB, collectionName)
                if mongoDBCollection is not None:
                    self.logger.debug("Collection [{}] found.".format(collectionName))
                else:
                    self.logger.debug("Collection [{}] not found, try to create it.".format(collectionName))
                    if not schemaTimeseriesMeta:
                        mongoDBCollection = mongoDB.create_collection(collectionName)
                    else:
                        mongoDBCollection = mongoDB.create_collection(
                            collectionName,
                            timeseries = schemaTimeseriesMeta)

            except BaseException as Error:
                errMsg = "Could not get/create collection: {} - [{}]".format(collectionName, Error)
                print(errMsg)
                self.logger.error(errMsg)
                retValue = mdbhReturnValue.FAILURE

        return retValue, mongoDBCollection

    def getCollection(self, mongoDB:Database, collectionName:str, schemaTimeseriesMeta=None) -> tuple[mdbhReturnValue, Collection]:
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        mongoDBCollection : Collection

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                if not schemaTimeseriesMeta:
                    mongoDBCollection = mongoDB[collectionName]
            except BaseException as Error:
                print ("Could not get/create collection: {} {}".format(collectionName, Error))
                retValue = mdbhReturnValue.FAILURE

        return retValue, mongoDBCollection

    def getDoc(self, mongoDBCollection : Collection, query : Any|RawBSONDocument) -> tuple[mdbhReturnValue, Cursor, list[dict]]:
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        mongoDBDoc : Cursor
        mongoDBDocList : list[dict] = []

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                mongoDBDoc = mongoDBCollection.find(query)
                mongoDBDocList = list(mongoDBDoc)
            except BaseException as Error:
                print ("Could not query document, query: {} - [{}]".format(
                    query,
                    Error
                ))
                retValue = mdbhReturnValue.FAILURE

        return retValue, mongoDBDoc, mongoDBDocList

    def insertDoc(self, mongoDBCollection : Collection, docDict : Any | RawBSONDocument) -> tuple[mdbhReturnValue, InsertOneResult]:
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        docRecordId : InsertOneResult

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                docRecordId = mongoDBCollection.insert_one(docDict)

            except BaseException as Error:
                errMsg = "Could not insert document: {} - [{}]".format(
                    docDict,
                    Error
                )
                print(errMsg)
                self.logger.error(errMsg)
                retValue = mdbhReturnValue.FAILURE

        return retValue, docRecordId
    
    # create new if not exist, keep _id() if existing: https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.replace_one 
    #   e.g. filter ={ "uuid": docDict['uuid'] }
    def replaceDoc(self, mongoDBCollection : Collection, docDict : Any | RawBSONDocument, filter : dict) -> tuple[mdbhReturnValue, UpdateResult]:
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        docRecordId : UpdateResult

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                # create if it does not exist, upsert=True
                docRecordId = mongoDBCollection.replace_one(
                    filter = filter,
                    replacement=docDict,
                    upsert=True)

            except BaseException as Error:
                errMsg = "Could not replace document: {} with filter [{}] - [{}]".format(
                    docDict,
                    filter,
                    Error
                )
                print(errMsg)
                self.logger.error(errMsg)
                retValue = mdbhReturnValue.FAILURE

        return retValue, docRecordId

    def insertManyDocs(self, mongoDBCollection : Collection, docDictList : Iterable[Any | RawBSONDocument]) -> tuple[mdbhReturnValue, InsertManyResult]:
        retValue : mdbhReturnValue = mdbhReturnValue.OK
        docRecordId : InsertManyResult

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                docRecordId = mongoDBCollection.insert_many(docDictList)

            except BaseException as Error:
                errMsg = "Could not insert document list: {} - [{}]".format(
                    docDictList,
                    Error
                )
                print(errMsg)
                self.logger.error(errMsg)
                retValue = mdbhReturnValue.FAILURE

        return retValue, docRecordId
            
    def clearCache(self, mongoDB:Database, collectionName:str) -> mdbhReturnValue:
        retValue : mdbhReturnValue = mdbhReturnValue.OK

        if not self.isFunctional():
            print("*ERR* : mongo DB not initialized.")
            retValue = mdbhReturnValue.CLIENT_FAILURE
        else:
            # create clean starting point
            try:
                mongoDB.command(
                    {
                        "planCacheClear": collectionName
                    }
                )

            except BaseException as Error:
                errMsg = "Could not clear cache of collection : {} - [{}]".format(
                    collectionName,
                    Error
                )
                print(errMsg)
                self.logger.error(errMsg)
                retValue = mdbhReturnValue.FAILURE

        return retValue
