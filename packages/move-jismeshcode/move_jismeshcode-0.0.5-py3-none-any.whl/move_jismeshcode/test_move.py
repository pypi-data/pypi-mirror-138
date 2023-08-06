# -*- coding: utf-8 -*-
import unittest
from move import move, _calcWithBase

class TestMove(unittest.TestCase):
    """test class of move.py
    """

    def test_moveLv1(self):
        """lv1
        """
        actual = move(5438, 3, 6)
        self.assertEqual(6041, actual)

    def test_moveLv2(self):
        """lv2
        """
        actual = move(543823, 4, -6)
        self.assertEqual(533930, actual)

    def test_moveLv3(self):
        """lv3
        """
        actual = move(54382343, 4, -6)
        self.assertEqual(54381387, actual)

    def test_moveLv4(self):
        """lv4
        """
        actual = move(543823431, 4, -6)
        self.assertEqual(543823151, actual)

    def test_moveLv5(self):
        """lv5
        """
        actual = move(5438234312, 2, 6)
        self.assertEqual(5438235342, actual)

    def test_moveLv5_2(self):
        """lv5
        """
        actual = move(5339770933, 0, 0)
        self.assertEqual(5339770933, actual)

    def test_moveLv6(self):
        """lv6
        """
        actual = move(54382343123, 5, 3)
        self.assertEqual(54382343422, actual)

    def test_calcWithBase(self):
        """test method for _calcWithBase
        """

        num, kuriagari = _calcWithBase(3, 10, 10)
        self.assertEqual(3, num)
        self.assertEqual(1, kuriagari)

    def test_calcWithBaseMinus1(self):
        """test method for _calcWithBase
        """

        num, kuriagari = _calcWithBase(0, -9, 10)
        self.assertEqual(1, num)
        self.assertEqual(-1, kuriagari)

    def test_calcWithBaseMinus2(self):
        """test method for _calcWithBase
        """

        num, kuriagari = _calcWithBase(0, -10, 10)
        self.assertEqual(0, num)
        self.assertEqual(-1, kuriagari)

    def test_calcWithBaseMinus3(self):
        """test method for _calcWithBase
        """

        num, kuriagari = _calcWithBase(0, -11, 10)
        self.assertEqual(9, num)
        self.assertEqual(-2, kuriagari)

    def test_calcWithBase7Minus(self):
        """test method for _calcWithBase
        """

        num, kuriagari = _calcWithBase(3, -10, 7)
        self.assertEqual(0, num)
        self.assertEqual(-1, kuriagari)
