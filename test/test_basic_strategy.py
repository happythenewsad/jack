import unittest




from BasicStrategy import BasicStrategy as bs
from Card import Card
from Utils import Utils as ut


class Tester(unittest.TestCase):

    def test_soft_lookups(self):
        c1 = Card('HA')
        c2 = Card('C2')
        upcard = Card('D6')

        row = bs.lookup_soft_row([c1,c2])
        col = bs.lookup_upcard_idx(upcard)

        self.assertEqual(row, 5)
        self.assertEqual(col, 4)

    def test_soft_with_A3A(self):
        c1 = Card('HA')
        c2 = Card('C3')
        c3 = Card('DA')

        row = bs.lookup_soft_row([c1,c2, c3])
        self.assertEqual(row, 4)
        # A 3 A => A4 => 15
        # Raw value: 25 

    def test_reg_lookups(self):
        c1 = Card('H6')
        c2 = Card('C7')
        upcard = Card('DA')

        row = bs.lookup_normal_row([c1,c2])
        col = bs.lookup_upcard_idx(upcard)
        self.assertEqual(row, 3)
        self.assertEqual(col, 9)

    def test_split_lookups(self):
        c1 = Card('H2')
        c2 = Card('C2')
        upcard = Card('D2')

        row = bs.lookup_split_row([c1,c2])
        col = bs.lookup_upcard_idx(upcard)
        self.assertEqual(row, 8)
        self.assertEqual(col, 0)

    def test_dealer_lookups(self):
        upcard = Card('S9')
        col = bs.lookup_upcard_idx(upcard)
        self.assertEqual(col, 7)