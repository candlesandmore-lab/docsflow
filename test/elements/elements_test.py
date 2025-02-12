#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from python.elements.datetimeItem import DatetimeItem
from python.elements.updateItem import UpdateItem, UpdateType
from python.infra.timeStampMeta import utcDateTime

class TestElements(unittest.TestCase):

    def test_datetimeStream(self):
        when=DatetimeItem(utcDateTime())
        print(dict(when))
        print(when.streamJson())

    def test_createAndStreamSingle(self):
        updateItem = UpdateItem(
            kind=UpdateType.CREATE,
            when=DatetimeItem(utcDateTime()),
            who='frankar',
            description="PV test for a single update element"
        )
        self.assertNotEqual(updateItem, None)
        print("Item streamed : ")
        print("{}".format(
            updateItem.streamJson()
        ))


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
