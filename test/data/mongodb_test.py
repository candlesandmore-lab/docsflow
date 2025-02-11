import unittest   # The test framework
import pymongo

import python.data.dataMongoDB as dataMongoDB

pv_mongoDBHost = "localhost"
pv_mongoDBPort = 27017
pv_mongoDBName = "pv_DocsFlow"
pv_mongoCollectionName = "pv_ProjectNodes"

# Data for none time series trials
'''
pv_NestedCollectionName = "Candles"
pv_IndicatorsCandles = {
    "Candles" : []
}

pv_CandleSeries1 = {
    "Indicator" : "MyStock",
    "10TradeCandles" : []
}

pv_CandleSeries2 = {
    "Indicator" : "MyBitcoin",
    "TimeWindowTradeCandles" : []
}

'''
pv_Node1 = {
    'Name' : 'pv_Node1',
    'type' : 'document',
    'timestamp' : 1222222.3,
    'description': 'PV node',
    'status': 'complete',
    'URL': 'C:\\Users\\Frank\\.gitconfig'
}
pv_Node2 = {
    'Name' : 'pv_Node2',
    'type' : 'context',
    'timestamp': 1202510311.305,
    'description': 'PV node',
    'status': 'complete',
    'URL': 'C:\\Users\\Frank\\somedir'
}
pv_Node3 = {
    'Name' : 'pv_Node3',
    'type' : 'context',
    'timestamp': 12025111.305,
    'description': 'PV node',
    'status': 'partial',
    'URL': 'C:\\Users\\Frank\\someverystrangedir'
}


pv_FailQuery = { "Name": "pv_NodeXYZ" }
pv_PassQueryMultiple = { "type": "context" }
pv_PassQuerySingle = { "type": "context" , 'timestamp' : { "$gt": 1202510300 }}

class Test_MongoDBInfra(unittest.TestCase):

    def test_mongoDBInfra(self):
        dbClient = dataMongoDB.initDB(pv_mongoDBHost, pv_mongoDBPort)
        self.assertNotEqual(dbClient, None)

        db = dataMongoDB.getDB(dbClient, pv_mongoDBName)
        self.assertNotEqual(db, None)

        collection = dataMongoDB.getCollection(db, pv_mongoCollectionName)
        self.assertNotEqual(collection, None)

        # create starting point
        collection.drop()
                
        _ = collection.insert_one(pv_Node1)
        _ = collection.insert_one(pv_Node2)
        _ = collection.insert_one(pv_Node3)

        queryDoc, queryDocList = dataMongoDB.getDoc(collection, pv_FailQuery)
        self.assertEqual(len(queryDocList), 0)

        queryDoc, queryDocList = dataMongoDB.getDoc(collection, pv_PassQueryMultiple)
        self.assertEqual(len(queryDocList), 2)
        print(queryDocList)
        
        queryDoc, queryDocList = dataMongoDB.getDoc(collection, pv_PassQuerySingle)
        self.assertEqual(len(queryDocList), 1)
        print(queryDocList)

    def test_plainMongoDB(self):
        
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        # create clean starting point
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        mycol.drop()
        mycol = mydb["customers"]

        mydict = { "name": "John", "address": "Highway 37" }

        x = mycol.insert_one(mydict)

        myquery = { "address": "Park Lane 38" }
        mydoc = mycol.find(myquery)
        resultList = list(mydoc)
        self.assertEqual(len(resultList), 0)

        myquery = { "address": "Highway 37" }
#        myquery = { "address": { "$regex": "^H" }}

        mydoc = mycol.find(myquery)
        resultList = list(mydoc)
        self.assertEqual(len(resultList), 1)

        for x in resultList:
            print(x)  

        print(myclient.list_database_names())

        myquery = { "address": "Mountain 21" }
        mycol.delete_one(myquery)
    '''
    def test_mongoDBTimeSeriesCollection(self):
        dbClient = dataMongoDB.initDB(pv_mongoDBHost, 27999)
        self.assertEqual(dbClient, None)

        dbClient = dataMongoDB.initDB(pv_mongoDBHost, pv_mongoDBPort)
        self.assertNotEqual(dbClient, None)

        db = dataMongoDB.getDB(dbClient, pv_mongoDBName)
        self.assertNotEqual(db, None)

        # https://www.codingforentrepreneurs.com/blog/time-series-with-python-mongodb-guide/


        collection = dataMongoDB.createCollection(
            db, 
            pv_NestedCollectionName,
            schemaTimeseriesMeta = pv_schemaTimeseriesMeta
            )
        self.assertNotEqual(collection, None)

        # create starting point
        collection.drop()
        
        id = dataMongoDB.insertDoc(collection, pv_CandleTimestamp1)
        self.assertNotEqual(id, None)
        id = dataMongoDB.insertDoc(collection, pv_CandleTimestamp2)
        self.assertNotEqual(id, None)
        id = dataMongoDB.insertDoc(collection, pv_CandleTimestamp3)
        self.assertNotEqual(id, None)

        # get all from one type
        resultList = list(collection.find({"metaData.symbol": "MyBitcoin"}))

        self.assertEqual(len(resultList), 2)
        for x in resultList:
            print(x)  
        print("#####################")        
        resultList = list(collection.find({"metaData.symbol": "MyStock"}))

        self.assertEqual(len(resultList), 1)
        for x in resultList:
            print(x) 
        print("#####################")

        resultList = list(collection.find({
            "metaData.symbol": "MyBitcoin",
            "metaData.candleType" : "Candle_10TradeCandles",
            "timestamp" : {'$gt': datetime.fromtimestamp(1202510000.305)}
        }))

        self.assertEqual(len(resultList), 1)
        for x in resultList:
            print(x)  

    def test_plainMongoDB(self):
        
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        # create clean starting point
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        mycol.drop()
        mycol = mydb["customers"]

        mydict = { "name": "John", "address": "Highway 37" }

        x = mycol.insert_one(mydict)

        myquery = { "address": "Park Lane 38" }
        mydoc = mycol.find(myquery)
        resultList = list(mydoc)
        self.assertEqual(len(resultList), 0)

        myquery = { "address": "Highway 37" }
#        myquery = { "address": { "$regex": "^H" }}

        mydoc = mycol.find(myquery)
        resultList = list(mydoc)
        self.assertEqual(len(resultList), 1)

        for x in resultList:
            print(x)  

        print(myclient.list_database_names())

        myquery = { "address": "Mountain 21" }
        mycol.delete_one(myquery)
    '''        
if __name__ == '__main__':
    unittest.main()

'''
# done for each candle type and indicator
        pv_IndicatorsCandles['Candles'].append(pv_CandleSeries1)
        pv_IndicatorsCandles['Candles'].append(pv_CandleSeries2)
        print(pv_IndicatorsCandles)
        id1 = collection.insert_one(pv_IndicatorsCandles)

        # update an array in the structure
        # rethink the data structure kyes == value
        #https://www.mongodb.com/community/forums/t/how-to-update-a-nested-document-use-operator-in-mongodb/170700/4
        # https://stackoverflow.com/questions/34431435/mongodb-update-an-object-in-nested-array
        collection = dataMongoDB.getCollection(db, pv_NestedCollectionName)
        collection.update_one(
            {
                'Candles.Indicator' : 'MyStock'
            },
            { 
                '$push' : { 'Candles.$.10TradeCandles': pv_Candle1 } 
            })
        collection.update_one(
            {
                'Candles.Indicator' : 'MyStock'
            },
            { 
                '$push' : { 'Candles.$.10TradeCandles': pv_Candle2 } 
            })
        collection.update_one(
            {
                'Candles.Indicator' : 'MyBitcoin'
            },
            { 
                '$push' : { 'Candles.$.TimeWindowTradeCandles': pv_Candle2 } 
            })
       # collection.updateOne(
        #    { Name: "MyStock" },
         #   { $push: { scores: { $each: [ 90, 92, 85 ] } } }
        # https://www.mongodb.com/docs/manual/tutorial/query-array-of-documents/
        collection = dataMongoDB.getCollection(db, pv_NestedCollectionName)

        pv_Candle1_fromDB = collection.find( 
            { 'Candles.Indicator': 'MyStock' }
            ,{ 'Candles.10TradeCandles' : 1 }  )
        print("BLOB")

        
        for candleDoc in list(pv_Candle1_fromDB):
            print(candleDoc)
            # not sure why, but the find returns
            #   the 10TradeCandles series AND an empty dictionary (that is for MyBitCoin)
            # 'Candles': [
            #       {'10TradeCandles': 
            #           [
            #               {'Name': 'pv_Foo', 'timestamp': 1202510311.305, 'high': 34.94, 'low': 30.987, 'volume': 3212}, 
            #               {'Name': 'pv_Foo', 'timestamp': 1202425373.404, 'high': 34.94, 'low': 30.987, 'volume': 3212}
            #           ]
            #       }, 
            #       {}]
            self.assertEqual(len(candleDoc['Candles'][0]['10TradeCandles']), 1)
            for candle in candleDoc['Candles'][0]['10TradeCandles']:
                print(candle)
'''