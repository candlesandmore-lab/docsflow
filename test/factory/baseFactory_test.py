#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.data.mongoDBHandler import mdbhReturnValue
from python.data.docsFlowFactory import DocsFlowFactory, dffReturnValue
from python.elements.baseNode import NodeType
from test.data.mongodb_test import PV_MongoHelper
from test.elements.tree_test import PV_TreeHelper

class TestFactory(unittest.TestCase):


    def test_createAndInsertProject(self):
        treeHelper = PV_TreeHelper()
        node = treeHelper.getHierNode()

        dbHelper = PV_MongoHelper()
        retValue, dbHandler = dbHelper.init_DBHandler()
        self.assertEqual(retValue, mdbhReturnValue.OK)

        docFlowFactory = DocsFlowFactory(
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        # PV ONLY : --- COLLECTION CLEAR ---
        retValue, collection = docFlowFactory.findCollection(node.nodeType)
        self.assertEqual(retValue, dffReturnValue.OK)
        collection.drop()
        # --- END OF COLLECTION CLEAR ---

        retValue = docFlowFactory.insertNode(
            node=node
        )
        self.assertEqual(retValue, dffReturnValue.OK)

        retValue = docFlowFactory.flushCaches()
        self.assertEqual(retValue, dffReturnValue.OK)

        retValue, listOfThings = docFlowFactory.getAnyNodeProperties(
            nodeType=NodeType.PROJECT,
            propertyKeys=['nodeType', 'uuid']
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print(listOfThings)

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
