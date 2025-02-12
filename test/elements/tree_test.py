#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.elements.baseNode import BaseNode
from python.elements.userItem import UserItem

class TestTrees(unittest.TestCase):


    def getBaseNode(self) -> BaseNode:
        node = BaseNode()
        return node
        
    def test_smallTreeStreamUnstream(self):
        node = self.getBaseNode()
        print(dict(node))

        child1 = self.getBaseNode()

        node.addChild(
            child=child1,
            user=UserItem('frankar', 'PV'))
        
        print(dict(node))


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
