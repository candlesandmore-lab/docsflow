import pymongo
import pymongo.errors


# dbLocation=some-host:port
def initDB(host="localhost", port=27017, replicaSet=None):

    if replicaSet == None:
        # e.g. mongodb://localhost:27017/"
        mongoDBClient = pymongo.MongoClient("mongodb://{}:{}/".format(host, port), 
            serverSelectionTimeoutMS = 2000, 
            tz_aware=True)
    else:
        mongoDBClient = pymongo.MongoClient("mongodb://{}:{}/".format(host, port), 
            serverSelectionTimeoutMS = 2000, 
            tz_aware=True,
            replicaSet=replicaSet)

    try:
        serverInfo = mongoDBClient.server_info() # will throw an exception
        print("*INFO* : connected successfully to [{}]".format(serverInfo))
    except BaseException  as Error:
        print ("Could not connect to server: {}:{} {}".format(host, port, Error))
        mongoDBClient = None
    
    return mongoDBClient

def getDB(mongoDBClient, dbName):

    if mongoDBClient == None:
        print("*ERR* : mongo DB client not initialized.")
    else:
        # create clean starting point
        try:
            mongoDB = mongoDBClient[dbName]
        except BaseException as Error:
            print ("Could not get/create database: {} {}".format(dbName, Error))
            mongoDB = None

    return mongoDB

def createCollection(mongoDB, collectionName, schemaTimeseriesMeta=None):
    if mongoDB == None:
        print("*ERR* : mongo DB not initialized.")
    else:
        # create clean starting point
        try:
            mongoDBCollection = getCollection(mongoDB, collectionName)
            if mongoDBCollection == None:
                if not schemaTimeseriesMeta:
                    mongoDBCollection = mongoDB.create_collection(collectionName)
                else:
                    mongoDBCollection = mongoDB.create_collection(
                        collectionName,
                        timeseries = schemaTimeseriesMeta)

        except BaseException as Error:
            print ("Could not get/create collection: {} {}".format(collectionName, Error))
            mongoDBCollection = None

    return mongoDBCollection

def getCollection(mongoDB, collectionName, schemaMeta=None):

    if mongoDB == None:
        print("*ERR* : mongo DB not initialized.")
    else:
        # create clean starting point
        try:
            if not schemaMeta:
                mongoDBCollection = mongoDB[collectionName]
        except BaseException as Error:
            print ("Could not get/create collection: {} {}".format(collectionName, Error))
            mongoDBCollection = None

    return mongoDBCollection

def getDoc(mongoDBCollection, query):
    if mongoDBCollection == None:
        print("*ERR* : getDocument() : mongo DB collection not initialized.")
    else:
        # create clean starting point
        try:
            mongoDBDoc = mongoDBCollection.find(query)
            mongoDBDocList = list(mongoDBDoc)
        except BaseException as Error:
            print ("Could not query document, query: {}".format(Error, query))
            mongoDBDoc = None
            mongoDBDocList = None

    return mongoDBDoc, mongoDBDocList

def insertDoc(mongoDBCollection, docDict):
    if mongoDBCollection == None:
        print("*ERR* : getDocument() : mongo DB collection not initialized.")
    else:
        # create clean starting point
        try:
            docRecordId = mongoDBCollection.insert_one(docDict)

        except BaseException as Error:
            print ("Could not insert document: {}".format(Error, docDict))
            docRecordId = None

    return docRecordId

def insertManyDocs(mongoDBCollection, docDictList):
    if mongoDBCollection == None:
        print("*ERR* : getDocument() : mongo DB collection not initialized.")
    else:
        # create clean starting point
        try:
            docRecordId = mongoDBCollection.insert_many(docDictList)

        except BaseException as Error:
            print ("Could not insert document list: {}".format(Error, docDictList))
            docRecordId = None

    return docRecordId
    