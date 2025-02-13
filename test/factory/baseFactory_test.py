#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.data.mongoDBHandler import mdbhReturnValue
from python.data.docsFlowFactory import DocsFlowFactory, dffReturnValue
from python.elements.baseNode import NodeType
from python.elements.userItem import UserItem
from test.data.mongodb_test import PV_MongoHelper
from test.elements.tree_test import PV_TreeHelper

class TestFactory(unittest.TestCase):


    def test_createInsertGetProject(self):
        treeHelper = PV_TreeHelper()
        node1 = treeHelper.getHierNode()
        node2 = treeHelper.getHierNode()

        dbHelper = PV_MongoHelper()
        retValue, dbHandler = dbHelper.init_DBHandler()
        self.assertEqual(retValue, mdbhReturnValue.OK)

        docFlowFactory = DocsFlowFactory(
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        # PV ONLY : --- COLLECTION CLEAR ---
        retValue, collection = docFlowFactory.findCollection(node1.nodeType)
        self.assertEqual(retValue, dffReturnValue.OK)
        collection.drop()
        # --- END OF COLLECTION CLEAR ---

        retValue = docFlowFactory.insertNode(
            node=node1
        )
        self.assertEqual(retValue, dffReturnValue.OK)

        retValue = docFlowFactory.insertNode(
            node=node2
        )
        self.assertEqual(retValue, dffReturnValue.OK)

        retValue = docFlowFactory.flushCaches()
        self.assertEqual(retValue, dffReturnValue.OK)

        # list user significant properties
        retValue, listOfThings = docFlowFactory.getAnyNodeProperties(
            nodeType=NodeType.PROJECT,
            propertyKeys=['uuid', 'name']
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print(listOfThings)

        # select one and get full tree
        self.assertEqual(len(listOfThings), 2)
        # user selects entry #1
        retValue, nodeFromDB = docFlowFactory.getNode(
            listOfDocProperties=listOfThings,
            index=1
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print("##### FROM DB ##########")
        print(dict(nodeFromDB))

        if nodeFromDB.uuid == node1.uuid:
            print("### FROM BL created ###")
            print(dict(node1))
            self.assertEqual(dict(nodeFromDB), dict(node1))
        else:
            print("### FROM BL created ###")
            print(dict(node2))
            self.assertEqual(dict(nodeFromDB), dict(node2))

    def test_createInsertGetUpdateProject(self):
        treeHelper = PV_TreeHelper()
        node1 = treeHelper.getHierNode()
        node2 = treeHelper.getHierNode()

        dbHelper = PV_MongoHelper()
        retValue, dbHandler = dbHelper.init_DBHandler()
        self.assertEqual(retValue, mdbhReturnValue.OK)

        docFlowFactory = DocsFlowFactory(
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        # PV ONLY : --- COLLECTION CLEAR ---
        retValue, collection = docFlowFactory.findCollection(node1.nodeType)
        self.assertEqual(retValue, dffReturnValue.OK)
        collection.drop()
        # --- END OF COLLECTION CLEAR ---

        retValue = docFlowFactory.insertNode(
            node=node1
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print("*PV* : inserted top node with UUID[{}].".format(node1.uuid))

        retValue = docFlowFactory.insertNode(
            node=node2
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print("*PV* : inserted top node with UUID[{}].".format(node2.uuid))

        retValue = docFlowFactory.flushCaches()
        self.assertEqual(retValue, dffReturnValue.OK)

        # list user significant properties
        retValue, listOfThings = docFlowFactory.getAnyNodeProperties(
            nodeType=NodeType.PROJECT,
            propertyKeys=['uuid', 'name']
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        # print(listOfThings)

        # select one and get full tree
        self.assertEqual(len(listOfThings), 2)
        # user selects entry #1
        retValue, nodeFromDB = docFlowFactory.getNode(
            listOfDocProperties=listOfThings,
            index=1
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        #print("##### FROM DB ##########")
        #print(dict(nodeFromDB))
        print("*PV* : got top node from DB with UUID[{}].".format(nodeFromDB.uuid))

        if nodeFromDB.uuid == node1.uuid:
            print("### FROM BL created ###")
            #print(dict(node1))
            self.assertEqual(dict(nodeFromDB), dict(node1))
        else:
            print("### FROM BL created ###")
            #print(dict(node2))
            self.assertEqual(dict(nodeFromDB), dict(node2))

        print("  +-- node matches the one we inserted.")
        # BL updates some fields
        #  (a) add child to top
        print("*PV* : updated node with UUID[{}] in BL.".format(nodeFromDB.uuid))
        childAdded = treeHelper.getBaseNode(NodeType.CONTEXT)

        nodeFromDB.addChild(
            child=childAdded,
            user=UserItem('test_createInsertGetUpdateProject', 'UNITTEST'))
        
        # (b) add TASK child to existing child
        
        childAdded = treeHelper.getBaseNode(NodeType.TASK)
        nodeFromDB.childs[0].addChild(
            child=childAdded,
            user=UserItem('test_createInsertGetUpdateProject', 'UNITTEST'))

        retValue = docFlowFactory.updateNode(
            nodeFromDB
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print("*PV* : updated top node in DB with UUID[{}].".format(nodeFromDB.uuid))



if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
