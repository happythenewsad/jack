import unittest

from Card import Card
from Player import Player
from Shoe import Shoe
from Hand import Hand

class ShoeTester(unittest.TestCase):

    def test_gen_cards(self):
        shoe = Shoe()
        self.assertEqual(len(shoe.cards), 8*52)
        self.assertEqual(type(shoe.cards[0]), Card)

    def test_end_of_shoe(self):
        shoe = Shoe()
        [shoe.pop() for iter in range(416)]
        self.assertEqual(shoe.end_of_shoe, False)
        shoe.pop()
        self.assertEqual(shoe.end_of_shoe, True)
        self.assertEqual(len(shoe.cards), 0)

    def test_removeCards(self):
        # removes 2 cards
        shoe = Shoe()
        shoe.cards = [Card('H10'), Card('CJ'), Card('D2')]

        result = shoe.removeCards(set([10]), 2)
        self.assertEqual(result, True)
        self.assertEqual(set([c.name for c in shoe.cards]), set(['D2']) )
        
        result = shoe.removeCards(set([10]), 1)
        self.assertEqual(set([c.name for c in shoe.cards]), set(['D2']) )
        self.assertEqual(result, False)

        #removeCards should not remove too many cards
        shoe = Shoe()
        shoe.cards = [Card('H9'), Card('C9'), Card('D2')]

        result = shoe.removeCards(set([9]), 1)
        self.assertEqual(result, True)
        self.assertEqual(len(shoe.cards), 2 )

        # remove 1 card from large shoe 
        shoe = Shoe()
        shoe.removeCards(set([10]),1)
        self.assertTrue(len(shoe.cards), 415)

        #remove a card from a range of cards
        shoe = Shoe()
        shoe.cards = [Card('H10'), Card('CJ'), Card('D2')]
        result = shoe.removeCards(set([2,3,5]),1)
        self.assertEqual(result, True)
        self.assertEqual(set([c.name for c in shoe.cards]), set(['H10', 'CJ']) )