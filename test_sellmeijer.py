#!/usr/bin/python

import unittest

from sellmeijer import Sellmeijer, domino_calc

class SellmeijerTestCase(unittest.TestCase):
    """Tests the Sellmeijer script"""

    def test_usecase_1(self):
        """This usecase scores 3 positives and 1 negative on deklaagdikte < 2 and normklasse 1/300 - 1/1000"""
        S = Sellmeijer()
        S.boezempeil = 6.0
        S.slootpeil = 2.73
        S.d = 1.8
        S.d70_m= 2.08e-4
        S.L = 48.2
        S.d70 = 1.2e-4
        S.D = 54
        S.gamma_b = 1.
        S.k = 5.e-5

        S.gamma_p = 16.19

        #using non rep values
        #everything except deklaagdikte < 2 and normklasse 1/300 - 1/1000 should be fine
        self.assertTrue(S.calc(deklaagdikte = 1, normklasse=1, rep=False))
        self.assertTrue(S.calc(deklaagdikte = 2, normklasse=1, rep=False))
        #now check the only one that should not be ok
        self.assertFalse(S.calc(deklaagdikte = 1, normklasse=2, rep=False))
        self.assertTrue(S.calc(deklaagdikte = 2, normklasse=2, rep=False))

        #S.save_report("test1.pdf")

    def test_usecase_2(self):
        """This usecase scores all 4 negatives"""
        S = Sellmeijer()
        S.boezempeil = 6.0
        S.slootpeil = 2.73
        S.d = 1.8
        S.d70_m= 2.08e-4
        S.L = 48.2
        S.d70 = 1.2e-4
        S.D = 54
        S.gamma_b = 1.
        S.k = 5.e-5

        S.gamma_p = 16.19

        #using rep values
        #everything should be False
        self.assertFalse(S.calc(deklaagdikte = 1, normklasse=1))
        self.assertFalse(S.calc(deklaagdikte = 2, normklasse=1))
        self.assertFalse(S.calc(deklaagdikte = 1, normklasse=2))
        self.assertFalse(S.calc(deklaagdikte = 2, normklasse=2))

        #S.save_report("test2.pdf")

    def test_usecase_3(self):
        """This usecase should return false, true and is based on the option to include all mandatory parameters in the functioncall"""
        S = Sellmeijer()
        self.assertFalse(S.calc_from_params(boezempeil=6.0, slootpeil=2.73, d=1.8, d70_m=2.08e-4, L=48.2, d70=1.2e-4, D=54, gamma_b=1, k=5e-5, deklaagdikte=1, normklasse=2, rep=False))
        self.assertTrue(S.calc_from_params(boezempeil=6.0, slootpeil=2.73, d=1.8, d70_m=2.08e-4, L=48.2, d70=1.2e-4, D=54, gamma_b=1, k=5e-5, deklaagdikte=1, normklasse=1, rep=False))

    def test_domino_usecase(self):
        """This usecase simulates the API call from the domino environment"""
        self.assertFalse(domino_calc(boezempeil=6.0, slootpeil=2.73, d=1.8, d70_m=2.08e-4, L=48.2, d70=1.2e-4, D=54, gamma_b=1, k=5e-5, deklaagdikte=1, normklasse=2, rep=False))
        self.assertTrue(domino_calc(boezempeil=6.0, slootpeil=2.73, d=1.8, d70_m=2.08e-4, L=48.2, d70=1.2e-4, D=54, gamma_b=1, k=5e-5, deklaagdikte=1, normklasse=1, rep=False))

if __name__=="__main__":
    unittest.main()
