#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import unittest
from zoneinfo import ZoneInfo

from python.infra import timeStampMeta

class TimestampTests(unittest.TestCase):

    def test_getUTC(self):
        utcTimestamp : datetime = timeStampMeta.utcDateTime()
        print(utcTimestamp)

        
        Los_Angeles_Timestamp = datetime.now(ZoneInfo("America/Los_Angeles"))
        print(Los_Angeles_Timestamp)
        print(timeStampMeta.utcDateTime(Los_Angeles_Timestamp))
        
        self.assertEqual(1, 1)  # a == b


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
