import unittest

from Card import Card
from Player import Player
from Shoe import Shoe
from Hand import Hand
from Utils import Utils

class ShoeTester(unittest.TestCase):
    def test_has_soft_total(self):
        cards = [Card('HA'), Card('C3'), Card('C3')]
        self.assertEqual(Utils.has_soft_total(cards), True)

        cards = [Card('HA'), Card('C3'), Card('C3'), Card('C6')]
        self.assertEqual(Utils.has_soft_total(cards), False)

    def test_card_value(self):
        cards = [Card('HA'), Card('C3'), Card('C3')]
        self.assertEqual(Utils.card_value(cards), 17)

        cards.append(Card('H5'))

        self.assertEqual(Utils.card_value(cards), 12)

    def test_card_value_multiple_aces(self):
        cards = [Card('HA'), Card('DA'), Card('SA'), Card('C10'), Card('C7')]
        self.assertEqual(Utils.card_value(cards), 20)