#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.data.docsFlowFactory import DocsFlowFactory, dffReturnValue
from python.data.mongoDBHandler import mdbhReturnValue
from python.elements.baseNode import NodeReturnValue, NodeType
from python.elements.userItem import UserItem
from python.flows.docsFlow.projectNode import ProjectNode
from test.data.mongodb_test import PV_MongoHelper

class PV_ProjectHelper():
    def __init__(self, path:str):
        self.projectNode = ProjectNode(
            name="PV_projectForConstructionTest",
            nodeType=NodeType.PROJECT
        )

        self.importStatus = self.projectNode.importFolderContent(
            folder=path,
            user=UserItem(
                name="PV_testcase__project_test",
                role="TESTER"
            )
        )        

    def getProjectNode(self) -> ProjectNode:
        return self.projectNode   

class TestProjects(unittest.TestCase):

    def test_projectConstructionByFolders(self):
        projectHelper = PV_ProjectHelper(
            path = r'C:\Users\Frank\SynologyDrive\Drive\LaptopOnly\Steuer\2024'
        )
        self.assertEqual(projectHelper.importStatus, NodeReturnValue.OK)
        projectDict = projectHelper.getProjectNode().toDict()
        print(projectDict)

    def test_createInsertGetRealProject(self):
        projectHelper = PV_ProjectHelper(
            path = r'C:\Users\Frank\SynologyDrive\Drive\LaptopOnly\Steuer\2024'
        )
        self.assertEqual(projectHelper.importStatus, NodeReturnValue.OK)

        projectNode = projectHelper.getProjectNode()

        dbHelper = PV_MongoHelper()
        retValue, dbHandler = dbHelper.init_DBHandler()
        self.assertEqual(retValue, mdbhReturnValue.OK)

        docFlowFactory = DocsFlowFactory(
            mongoDBHandler=dbHandler,
            dbName="pv_FactoryTests"
        )

        self.assertTrue(docFlowFactory.isFunctional())

        # PV ONLY : --- COLLECTION CLEAR ---
        retValue, collection = docFlowFactory.findCollection(projectNode.nodeType)
        self.assertEqual(retValue, dffReturnValue.OK)
        collection.drop()
        # --- END OF COLLECTION CLEAR ---

        retValue = docFlowFactory.updateNode(
            node=projectNode
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        print("*PV* : inserted top node with UUID[{}].".format(projectNode.uuid))

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
        self.assertEqual(len(listOfThings), 1)
        # user selects entry #1
        retValue, nodeFromDB = docFlowFactory.getNode(
            listOfDocProperties=listOfThings,
            index=0
        )
        self.assertEqual(retValue, dffReturnValue.OK)
        #print("##### FROM DB ##########")
        #print(nodeFromDB.toDict())
        print("*PV* : got top node from DB with UUID[{}].".format(nodeFromDB.uuid))

        self.maxDiff = None
        self.assertEqual(nodeFromDB.toDict(),projectNode.toDict())

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
