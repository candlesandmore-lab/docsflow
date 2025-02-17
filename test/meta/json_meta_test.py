#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from python.flows.meta.metaReaderJson import MetaReaderJson

class TestJsonMeta(unittest.TestCase):


    def test_importMeta(self):
        metaReader = MetaReaderJson()
        success, metaFromDir = metaReader.importFolderMetadata(
            folder=r'C:\Users\Frank\SynologyDrive\Drive\LaptopOnly\github\docsflow\test\meta\testData'
        )
        self.assertTrue(success)

        print(metaFromDir)

        self.assertEqual(1, 1)  # a == b


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
