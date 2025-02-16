#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.data.docFlowNodeFactory import DocFlowNodeFactory
from python.data.mongoDBHandler import mdbhReturnValue
from python.data.mongoDBFactory import MongoDBFactory, dffReturnValue
from python.elements.baseNode import NodeType
from python.elements.userItem import UserItem
from python.flows.docsFlow.contextNode import ContextNode
from test.data.mongodb_test import PV_MongoHelper
from test.elements.tree_test import PV_TreeHelper

class TestFactory(unittest.TestCase):


    def test_createInsertGetProject(self):
        treeHelper = PV_TreeHelper()
        node1 = treeHelper.getProjectDocHierNode()
        node2 = treeHelper.getProjectDocHierNode()

        dbHelper = PV_MongoHelper()
        retValue, dbHandler = dbHelper.init_DBHandler()
        self.assertEqual(retValue, mdbhReturnValue.OK)

        docFlowFactory = MongoDBFactory(
            nodeFactory=DocFlowNodeFactory(),
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        # PV ONLY : --- COLLECTION CLEAR ---
        retValue, collection = docFlowFactory.findCollection(node1.nodeType)
        self.assertEqual(retValue, dffReturnValue.OK)
        collection.drop()
        # --- END OF COLLECTION CLEAR ---

        retValue = docFlowFactory.updateNode(
            node=node1
        )
        self.assertEqual(retValue, dffReturnValue.OK)

        retValue = docFlowFactory.updateNode(
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
        print(nodeFromDB.toDict())

        if nodeFromDB.uuid == node1.uuid:
            print("### FROM BL created ###")
            print(node1.toDict())
            self.assertEqual(nodeFromDB.toDict(),node1.toDict())
        else:
            print("### FROM BL created ###")
            print(node2.toDict())
            self.assertEqual(nodeFromDB.toDict(),node2.toDict())

    def test_createInsertGetUpdateProject(self) -> None:
        treeHelper = PV_TreeHelper()
        node1 = treeHelper.getProjectDocHierNode()
        node2 = treeHelper.getProjectDocHierNode()

        dbHelper = PV_MongoHelper()
        mdbhRetValue, dbHandler = dbHelper.init_DBHandler()
        self.assertEqual(mdbhRetValue, mdbhReturnValue.OK)

        docFlowFactory = MongoDBFactory(
            nodeFactory=DocFlowNodeFactory(),
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        # PV ONLY : --- COLLECTION CLEAR ---
        dffRetValue, collection = docFlowFactory.findCollection(node1.nodeType)
        self.assertEqual(dffRetValue, dffReturnValue.OK)
        collection.drop()
        # --- END OF COLLECTION CLEAR ---

        dffRetValue = docFlowFactory.updateNode(
            node=node1
        )
        self.assertEqual(dffRetValue, dffReturnValue.OK)
        print("*PV* : inserted top node with UUID[{}].".format(node1.uuid))

        dffRetValue = docFlowFactory.updateNode(
            node=node2
        )
        self.assertEqual(dffRetValue, dffReturnValue.OK)
        print("*PV* : inserted top node with UUID[{}].".format(node2.uuid))

        dffRetValue = docFlowFactory.flushCaches()
        self.assertEqual(dffRetValue, dffReturnValue.OK)

        # list user significant properties
        dffRetValue, listOfThings = docFlowFactory.getAnyNodeProperties(
            nodeType=NodeType.PROJECT,
            propertyKeys=['uuid', 'name']
        )
        self.assertEqual(dffRetValue, dffReturnValue.OK)
        # print(listOfThings)

        # select one and get full tree
        self.assertEqual(len(listOfThings), 2)
        # user selects entry #1
        dffRetValue, nodeFromDB = docFlowFactory.getNode(
            listOfDocProperties=listOfThings,
            index=1
        )
        self.assertEqual(dffRetValue, dffReturnValue.OK)
        #print("##### FROM DB ##########")
        #print(nodeFromDB.toDict())
        print("*PV* : got top node from DB with UUID[{}].".format(nodeFromDB.uuid))

        if nodeFromDB.uuid == node1.uuid:
            print("### FROM BL created ###")
            #print(node1.toDict())
            self.assertEqual(nodeFromDB.toDict(),node1.toDict())
        else:
            print("### FROM BL created ###")
            #print(node2.toDict())
            self.assertEqual(nodeFromDB.toDict(),node2.toDict())

        print("  +-- node matches the one we inserted.")

        # BL updates some fields
        factory = DocFlowNodeFactory()

        #  (a) add child to top
        print("*PV* : updated node with UUID[{}] in BL.".format(nodeFromDB.uuid))

        # BL always uses factory for node creation
        contextChildAdded : ContextNode = factory.constructNode(NodeType.CONTEXT)
        contextChildAdded.name = "PV_baseFactory_addedTopContextChild"

        nodeFromDB.addOrUpdateChild(
            child=contextChildAdded,
            user=UserItem('test_createInsertGetUpdateProject', 'UNITTEST'))
        
        # (b) add TASK child to existing child
        # BL always uses factory for node creation
        taskChildAdded : ContextNode = factory.constructNode(NodeType.TASK)
        taskChildAdded.name = "PV_baseFactory_addedSubTaskChild"

        nodeFromDB.childs[0].addOrUpdateChild(
            child=taskChildAdded,
            user=UserItem('test_createInsertGetUpdateProject', 'UNITTEST'))

        dffRetValue = docFlowFactory.updateNode(
            nodeFromDB
        )

        self.assertEqual(dffRetValue, dffReturnValue.OK)
        print("*PV* : updated top node in DB with UUID[{}].".format(nodeFromDB.uuid))

        # read project node again and compare JSON to last inserted, e.g. with TASK
        dffRetValue, updatedNodeFromDB = docFlowFactory.getNode(
            listOfDocProperties=listOfThings,
            index=1
        )
        self.assertEqual(dffRetValue, dffReturnValue.OK)

        self.assertEqual(nodeFromDB.toDict(), updatedNodeFromDB.toDict())


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
