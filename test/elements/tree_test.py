#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import uuid

from python.elements.baseNode import BaseNode, NodeType
from python.elements.userItem import UserItem

class PV_TreeHelper():
    def __init__(self):
        pass
    
    def getBaseNode(self, nodeType : NodeType) -> BaseNode:
        node = BaseNode(
            name = "PV_TreeHelper_{}".format(uuid.uuid4()),
            nodeType=nodeType
        )
        return node
    
    def getHierNode(self) -> BaseNode:
        node = self.getBaseNode(NodeType.PROJECT)

        child1 = self.getBaseNode(NodeType.DOC)

        node.addChild(
            child=child1,
            user=UserItem('frankar', 'PV'))
    
        return node
        
class TestTrees(unittest.TestCase):
        
    def test_smallTreeStream(self):
        treeHelper = PV_TreeHelper()
        node = treeHelper.getHierNode()
        
        print(dict(node))

    def test_smallTreeStreamUnstream(self):
        treeHelper = PV_TreeHelper()
        node = treeHelper.getHierNode()
        
        #
        jsonStream = node.toJson()
        print(jsonStream)

        streamedNode = BaseNode()
        streamedNode.fromJson(
            jsonString=jsonStream
        )

        print(dict(streamedNode))

        self.assertDictEqual(dict(node), dict(streamedNode))
    


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
