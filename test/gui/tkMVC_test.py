#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.gui.controller import Controller
from python.gui.model import Model
from python.gui.view import View
from test.meta.json_meta_test import TestJsonMeta

class TestMVC_GUI(unittest.TestCase):


    def test_withStaticProject(self):
        pvHelper = TestJsonMeta() 
        projectNode = pvHelper.test_importProjectWithMetaDataTrafficLight()

        model = Model()
        view = View()
        controller = Controller(model, view)

        # TODO: user selected and DB loaded
        controller.model.projectModel.setNode(projectNode)

        controller.start()

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
