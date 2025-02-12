#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from python.elements.datetimeItem import DatetimeItem
from python.elements.streamableItem import StreamableItem
from python.elements.updateItem import UpdateItem, UpdateType
from python.infra.timeStampMeta import utcDateTime

class pvStream(StreamableItem):
    def __init__(self, when : DatetimeItem):
        super().__init__()
        self.when = when
        self.someText : str = "PV test"
        self.someNumber : int = 14041978

    
class TestElements(unittest.TestCase):

    def test_datetimeStream(self):
        when=DatetimeItem(utcDateTime())
        print(dict(when))
        print(when.toJson())

        # stream inside another class
        print("####################")
        streamParent = pvStream(when)
        print(dict(streamParent))
        print(streamParent.toJson())


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
            updateItem.toJson()
        ))

    def test_streamUnstreamSingle(self):
        updateItem = UpdateItem(
            kind=UpdateType.CREATE,
            when=DatetimeItem(utcDateTime()),
            who='frankar',
            description="PV test for a stream/update/unstream"
        )
        self.assertNotEqual(updateItem, None)
        initialJsonString = updateItem.toJson()
        print("Item streamed : ")
        print("{}".format(
            initialJsonString
        ))

        unstreamedItem = UpdateItem()
        unstreamedItem.fromJson(initialJsonString)

        unstreamedItemJsonString = unstreamedItem.toJson()
        print("Unstreamed #original: ")
        print("{}".format(
            unstreamedItemJsonString
        ))

        self.assertEqual(initialJsonString, unstreamedItemJsonString)
        self.assertDictEqual(json.loads(initialJsonString), json.loads(unstreamedItemJsonString))

        unstreamedItem.who = 'PV-overwrite-who'
        unstreamedItemJsonString = unstreamedItem.toJson()
        print("Unstreamed #updated: ")
        print("{}".format(
            unstreamedItemJsonString
        ))

        self.assertNotEqual(initialJsonString, unstreamedItemJsonString)

if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
