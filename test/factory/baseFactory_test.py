#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.data.mongoDBHandler import mdbhReturnValue
from python.data.docsFlowFactory import DocsFlowFactory, dffReturnValue
from test.data.mongodb_test import PV_MongoHelper
from test.elements.tree_test import PV_TreeHelper

class TestFactory(unittest.TestCase):


    def test_createAndInsertProject(self):
        treeHelper = PV_TreeHelper()
        node = treeHelper.getHierNode()

        dbHelper = PV_MongoHelper()
        retValue, dbHandler = dbHelper.init_DBHandler()
        self.assertTrue(retValue, mdbhReturnValue.OK)

        docFlowFactory = DocsFlowFactory(
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        retValue = docFlowFactory.insertNode(
            node=node
        )
        self.assertTrue(retValue, dffReturnValue.OK)

        retValue = docFlowFactory.flushCaches()
        self.assertTrue(retValue, dffReturnValue.OK)



if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
