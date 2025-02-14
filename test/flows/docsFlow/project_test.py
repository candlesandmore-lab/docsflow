#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.elements.baseNode import NodeType
from python.elements.userItem import UserItem
from python.flows.docsFlow.projectNode import ProjectNode

class TestProjects(unittest.TestCase):


    def test_projectConstructionByFolders(self):
        projectNode = ProjectNode(
            name="PV_projectForConstructionTest",
            nodeType=NodeType.PROJECT
        )

        projectNode.importFolderContent(
            folder=r'C:\Users\Frank\SynologyDrive\Drive\LaptopOnly\Steuer\2024',
            user=UserItem(
                name="PV_testcase__project_test",
                role="TESTER"
            )
        )
        print(dict(projectNode))


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
