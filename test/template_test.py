#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

class TestName(unittest.TestCase):


    def test_dummy(self):
        self.assertEqual(1, 1)  # a == b


if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
