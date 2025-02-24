#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from python.data.docFlowNodeFactory import DocFlowNodeFactory
from python.elements.baseNode import BaseNode, NodeReturnValue
from python.elements.streamableItem import StreamableDict, StreamableList
from python.elements.userItem import UserItem
from python.flows.meta.metaReaderJson import MetaReaderJson
from python.flows.status.baseNodeWithState import BaseNodeWithState
from python.flows.status.trafficLightState import TrafficLightState, TrafficLightStatusColor
from python.flows.ui.json.projectJsonUI import ProjectJsonUI
from test.elements.tree_test import PV_TreeHelper
from test.factory.baseFactory_test import TestFactory
from test.flows.docsFlow.project_test import PV_ProjectHelper

class TestJsonMeta(unittest.TestCase):

    def test_stream(self):
        thisList = StreamableList()
        thisList.append(["AVAILABLE", "2025-02-17T16:25:16"])
        thisList.append(["REVIEWED", "2025-02-18T16:25:16"])

        r = thisList.toList()
        print(r)

        thisDict = StreamableDict()
        thisDict["YEARLY_TRANSACTIONS"] = {
            "plan" : thisList
        }
        thisDict['name'] = "foo.bar"

        r = thisDict.toDict()
        print(json.dumps(r, indent=4))

    def test_importMeta(self):
        metaReader = MetaReaderJson()
        success, metaFromDir = metaReader.importFolderMetadata(
            folder=r'C:\Users\Frank\SynologyDrive\Drive\LaptopOnly\github\docsflow\test\meta\testData'
        )
        self.assertTrue(success)

        print(json.dumps(metaFromDir.toDict(), indent=4))
        print(metaFromDir.toJson())

    def test_importProjectWithMetaData(self) -> BaseNode:
        projectDir = r'C:\Users\Frank\SynologyDrive\Drive\LaptopOnly\github\docsflow\test\meta\testData'
        projectHelper = PV_ProjectHelper(
            path = projectDir
        )
        self.assertEqual(projectHelper.importStatus, NodeReturnValue.OK)

        #projectDict = projectHelper.getProjectNode().toDict()
        #print(projectDict)
   
        user = UserItem(
            name="FrankA",
            role="Steuerpflichtiger"
        )

        docNodeFactory = DocFlowNodeFactory()

        ui = ProjectJsonUI(
            user=user,
            docNodeFactory=docNodeFactory,
            project=projectHelper.getProjectNode(),
            metaDir=projectDir
        )

        self.assertTrue(ui.isFunctional())
        
        r = ui.project.toDict()

        testResult = "{}/test_importProjectWithMetaData.json".format(
            projectDir
        )
        with open(testResult, 'w', encoding='utf-8') as f:
            json.dump(r, f, ensure_ascii=False, indent=4)

        return ui.project

    def test_importProjectWithMetaDataTrafficLight(self):
        projectNode = self.test_importProjectWithMetaData()
        # map meta data to status
        self.assertTrue(isinstance(projectNode, BaseNodeWithState))

        success, overallState = projectNode.updateStateWithMetaData(
            path=""
        )

        self.assertTrue(success)
        print("*PV* : top state is [{}].".format(overallState))

        # calculate traffic light status
        trafficLightStateWorker = TrafficLightState()
        trafficLightStateWorker.updateStatus(node=projectNode, path="")
        print("*PV* : top status is [{}].".format(
            projectNode.getStatus(
                key=trafficLightStateWorker.id,
                default=TrafficLightStatusColor.RED
        )))
    
    def test_storeAndReadProjectWithMetaData(self):
        projectNode = self.test_importProjectWithMetaData()
        # 'create' 2nd node for sub-test
        treeHelper = PV_TreeHelper()
        node2 = treeHelper.getProjectDocHierNode()

        baseFactoryTest = TestFactory()
        baseFactoryTest.createInsertGetUpdate2Nodes(projectNode, node2)

        # TODO: implement and test status based on plan/status for nodes and roll up

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
