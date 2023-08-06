# -*- coding: utf-8 -*-
import unittest
from sub import sub

class TestSub(unittest.TestCase):
    """test class of sub.py
    """

    def test_subLv1(self):
        """lv1
        """
        actual = sub(6041, 5438)
        self.assertEqual((3, 6), actual)

    def test_subLv2(self):
        """lv2
        """
        actual = sub(533930, 543823)
        self.assertEqual((4, -6), actual)

    def test_subLv3(self):
        """lv3
        """
        actual = sub(54381387, 54382343)
        self.assertEqual((4, -6), actual)

    def test_subLv4(self):
        """lv4
        """
        actual = sub(543823151, 543823431)
        self.assertEqual((4, -6), actual)

    def test_subLv5(self):
        """lv5
        """
        actual = sub(5438235342, 5438234312)
        self.assertEqual((2, 6), actual)

    def test_subLv6(self):
        """lv6
        """
        actual = sub(54382343422, 54382343123)
        self.assertEqual((5, 3), actual)

