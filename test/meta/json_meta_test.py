#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from python.elements.streamableItem import StreamableDict, StreamableList
from python.flows.meta.metaReaderJson import MetaReaderJson

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

        self.assertEqual(1, 1)  # a == b


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
