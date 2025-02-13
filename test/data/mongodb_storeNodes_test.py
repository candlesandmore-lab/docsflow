#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from python.data import dataMongoDB
from python.elements.baseNode import BaseNode, NodeType
from test.data.mongodb_test import PV_MongoHelper
from test.elements.tree_test import PV_TreeHelper

pv_mongoNodeCollectionName = "pv_ProjectNodes"

class TestStoreNodes(unittest.TestCase):


    def test_storeHierNode(self):
        mongoDBHelper = PV_MongoHelper()
        db = mongoDBHelper.initPV_DB()

        self.assertNotEqual(db, None)

        collection = dataMongoDB.getCollection(db, pv_mongoNodeCollectionName)
        self.assertNotEqual(collection, None)

        # create starting point
        collection.drop()
                
        # create tree
        treeHelper = PV_TreeHelper()
        node = treeHelper.getHierNode()
        nodeDict = dict(node)
        print(nodeDict)

        docRecordId = dataMongoDB.insertDoc(collection, nodeDict)
        print(docRecordId)
        # _ = collection.insert_one(nodeDict)

        return db

    def test_retreiveProject(self):
        # construct and store node hierarchy
        db = self.test_storeHierNode()
        collection = dataMongoDB.getCollection(db, pv_mongoNodeCollectionName)

        # query all projects
        projectQuery = { "nodeType": 0 }
        queryDoc, queryDocList = dataMongoDB.getDoc(collection, projectQuery)
        self.assertNotEqual(len(queryDocList), 0)
        
        # reconstruct BL object tree
        projectDict = queryDocList[0]
        print(projectDict) # dict
        # TODO: move to BL
        #   - remove and remember MongoDB ID
        mongoId = projectDict.pop("_id")  # of type ObjectId

        retreivedNode = BaseNode(
            name="",
            nodeType=NodeType.PROJECT
        )
        retreivedNode.fromJson(
            jsonString=json.dumps(projectDict)
        )

        print(dict(retreivedNode))

        # test DB update
        updateResult = collection.update_one({"_id": mongoId}, {"$set" :{"uuid": "affe"}})
        print(updateResult)

        queryDoc, queryDocList = dataMongoDB.getDoc(collection, {"_id": mongoId})
        print(queryDocList[0])
        self.assertEqual(queryDocList[0]['uuid'], "affe")

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
