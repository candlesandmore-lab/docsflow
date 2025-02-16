#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import uuid

from python.data.baseNodeFactory import BaseNodeFactory
from python.data.docFlowNodeFactory import DocFlowNodeFactory
from python.elements.baseNode import BaseNode, NodeType
from python.elements.userItem import UserItem
from python.flows.docsFlow.docNode import DocNode
from python.flows.docsFlow.projectNode import ProjectNode

class PV_TreeHelper():
    def __init__(self):
        pass
    
    def getBaseNode(self) -> BaseNode:
        factory = BaseNodeFactory()

        node : BaseNode = factory.constructNode(NodeType.BASENODE)
        node.name = "PV_TreeHelper_BaseNode_{}".format(uuid.uuid4())

        return node
    
    def getProjectDocHierNode(self) -> BaseNode:

        factory = DocFlowNodeFactory()
        # project
        node : ProjectNode = factory.constructNode(NodeType.PROJECT)
        node.name = "PV_TreeHelper_ProjNode_{}".format(uuid.uuid4())
        
        # doc child
        child : DocNode = factory.constructNode(NodeType.DOC)
        child.name = "PV_TreeHelper_DocNode_{}".format(uuid.uuid4())

        node.addOrUpdateChild(
            child=child,
            user=UserItem('frankar', 'PV'))
    
        return node
        
class TestTrees(unittest.TestCase):
        
    def test_smallTreeStream(self) -> None:
        treeHelper = PV_TreeHelper()
        node = treeHelper.getBaseNode()
        
        print(node.toDict())

    def test_smallTreeStreamUnstream(self) -> None:
        treeHelper = PV_TreeHelper()
        node = treeHelper.getProjectDocHierNode()
        
        #
        jsonStream = node.toJson()
        print(jsonStream)

        # unstream from JSON, reconstructing the correct object types
        factory = DocFlowNodeFactory()
        streamedNode : ProjectNode = factory.constructNode(NodeType.PROJECT)
        streamedNode.fromJson(
            jsonString=jsonStream
        )

        print(streamedNode.toDict())

        self.assertDictEqual(node.toDict(), streamedNode.toDict())

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
