#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from python.data import dataMongoDB
from python.data.docFlowNodeFactory import DocFlowNodeFactory
from python.elements.baseNode import NodeType
from python.flows.docsFlow.projectNode import ProjectNode
from test.data.mongodb_test import PV_MongoHelper, pv_mongoDBName
from test.elements.tree_test import PV_TreeHelper
from pymongo.database import Database

pv_mongoNodeCollectionName = "pv_ProjectNodes"

class TestStoreNodes(unittest.TestCase):


    def test_storeHierNode(self) -> Database:
        mongoDBHelper = PV_MongoHelper()
        db = mongoDBHelper.initPV_DB()

        self.assertNotEqual(db, None)

        collection = dataMongoDB.getCollection(db, pv_mongoNodeCollectionName)
        self.assertNotEqual(collection, None)

        # create starting point
        collection.drop()
                
        # create tree
        treeHelper = PV_TreeHelper()
        node = treeHelper.getProjectDocHierNode()
        nodeDict = node.toDict()
        print(nodeDict)

        docRecordId = dataMongoDB.insertDoc(collection, nodeDict)
        print(docRecordId)

        print("*PV* : added PROJECT node to DB[{}] / COLLECTION [{}].".format(
            pv_mongoDBName,
            pv_mongoNodeCollectionName
        ))
        # _ = collection.insert_one(nodeDict)

        return db

    def test_retreiveProject(self) -> None:
        # construct and store node hierarchy
        db = self.test_storeHierNode()
        collection = dataMongoDB.getCollection(db, pv_mongoNodeCollectionName)

        # query all projects
        print("*PV* : query PROJECT nodes from DB[{}] / COLLECTION [{}].".format(
            pv_mongoDBName,
            pv_mongoNodeCollectionName
        ))
        projectQuery = { "nodeType" : "ProjectNode" }
        queryDoc, queryDocList = dataMongoDB.getDoc(collection, projectQuery)
        self.assertNotEqual(len(queryDocList), 0)
        
        # reconstruct BL object tree
        projectDict = queryDocList[0]
        print(projectDict) # dict

        #  This is part of the DB Factory in the real system
        mongoId = projectDict.pop("_id")  # of type ObjectId

        # This would be done in the DB factory later
        factory = DocFlowNodeFactory()
        retreivedNode : ProjectNode = factory.constructNode(NodeType.PROJECT)

        retreivedNode.fromJson(
            jsonString=json.dumps(projectDict)
        )

        print(retreivedNode.toDict())

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
