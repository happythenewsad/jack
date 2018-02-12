import unittest
import re
from Jack import Jack
from BasicStrategy import BasicStrategy as bs
from Card import Card
from Player import Player
from Shoe import Shoe
from Hand import Hand

class Tester(unittest.TestCase):

    def test_basic_stand_and_hit(self):
        p1 = Player(Hand([Card('HJ'), Card('HQ')]))
        upcard = Card('S2')
        shoe = []
        shoe.append(Card('CJ'))

        self.assertEqual(len(shoe), 1)
        Jack.turn(shoe, p1, 0, upcard)
        self.assertEqual(p1.hands[0].status, 'stand')
        self.assertEqual(len(shoe), 1)

        p2 = Player(Hand([Card('H3'), Card('H4')]))
        Jack.turn(shoe, p2, 0, upcard)

        self.assertEqual(p2.hands[0].status, 'stand')
        self.assertEqual(len(shoe), 0)

    def test_busted(self):
        p1 = Player(Hand([Card('HJ'), Card('HQ'), Card('H3')]))
        upcard = Card('S2')     
        shoe = [] 
        Jack.turn(shoe, p1, 0, upcard)
 
        self.assertEqual(p1.hands[0].status, 'busted')


    def test_blackjack(self):
        p1 = Player(Hand([Card('HQ'), Card('HA')]))
        upcard = Card('S2')     
        shoe = [] 
        Jack.turn(shoe, p1, 0, upcard)

        self.assertEqual(p1.hands[0].status, 'blackjack')


    def test_has_double(self):
        doublecards = [Card('H8'), Card('D8')]
        self.assertEqual(Jack.has_double(doublecards), True)

        notdoublecards = [Card('H8'), Card('H7')]
        self.assertEqual(Jack.has_double(notdoublecards), False)

    def test_soft_hit_then_stand(self):
        p1 = Player(Hand([Card('HA'), Card('H4')]))
        upcard = Card('S9')
        shoe = []
        shoe.append(Card('S4'))

        self.assertEqual(len(shoe), 1)
        result = Jack.turn(shoe, p1, 0, upcard)
        #result = result[0]
        self.assertEqual(p1.hands[0].status, 'stand')
        #self.assertEqual(result, 'stand')
        self.assertEqual(len(shoe), 0)

    def test_soft_stand(self): 
        p1 = Player(Hand([Card('HA'), Card('H9')]))
        upcard = Card('S4')
        shoe = []
        shoe.append(Card('H5'))

        result = Jack.turn(shoe, p1, 0, upcard)
        #result = result[0]
        self.assertEqual(p1.hands[0].status, 'stand')
        #self.assertEqual(result, 'stand')

    def test_soft_unnatural_blackjack(self): 
        p1 = Player(Hand([Card('HA'), Card('H4')]))
        upcard = Card('S5')
        shoe = []
        shoe.append(Card('H6'))

        result = Jack.turn(shoe, p1, 0, upcard)
        #result = result[0]
        self.assertEqual(p1.hands[0].status, 'ddown')
        #self.assertEqual(result, 'ddown')


    def test_split(self):
        p1 = Player(Hand([Card('H8'), Card('D8')]))
        upcard = Card('S2')     
        shoe = [] 
        shoe.append(Card('H9'))
        shoe.append(Card('H10'))

        self.assertEqual(len(p1.hands.keys()), 1)
        result = Jack.turn(shoe, p1, 0, upcard)

        self.assertEqual(len(p1.hands.keys()), 2)
        #self.assertEqual(result[0], 'stand')
        #self.assertEqual(result[1], 'stand')
        self.assertEqual(p1.hands[0].status, 'stand')
        self.assertEqual(p1.hands[1].status, 'stand')

        self.assertEqual(len(p1.hands[0].cards), 2)
        self.assertEqual(len(p1.hands[1].cards), 2)

        self.assertEqual(p1.hands[0].units, 1)
        self.assertEqual(p1.hands[1].units, 1)

    def test_soft(self):
        p1 = Player(Hand([Card('HA'), Card('C3'), Card('C3')]))
        upcard = Card('S2')     
        shoe = [] 
        shoe.append(Card('H9'))
        shoe.append(Card('H10'))

        Jack.turn(shoe, p1, 0, upcard)


    def test_doubledown(self):
        p1 = Player(Hand([Card('H4'), Card('H6')]))
        self.assertEqual(p1.hands[0].units, 1)
        upcard = Card('S2')     
        shoe = [] 
        shoe.append(Card('CJ'))

        self.assertEqual(len(shoe), 1)
        result = Jack.turn(shoe, p1, 0, upcard)
        #result = result[0]
        #self.assertEqual(result, 'ddown')
        self.assertEqual(p1.hands[0].status, 'ddown')
        self.assertEqual(len(shoe), 0)
        self.assertEqual(p1.hands[0].units, 2)

    def test_resolve_hands(self):
        # SCENARIO 1 - p1 busts, p2 wins normally
        p1 = Player()
        p2 = Player(Hand([Card('HJ'), Card('H9')]))

        p1.hands[0].status = 'busted'
        p2.hands[0].status = 'stand'

        self.assertEqual(p1.recent_winloss, [])
        self.assertEqual(p2.recent_winloss, [])

        dealer_cards = [Card('HJ'), Card('C7')] # no bust
        Jack.resolve_hands(p1, dealer_cards)
        Jack.resolve_hands(p2, dealer_cards)

        self.assertEqual(len(p1.recent_winloss), 1)
        self.assertEqual(len(p2.recent_winloss), 1)

        self.assertEqual(p1.recent_winloss[0], 0)
        self.assertEqual(p2.recent_winloss[0], 2)

        # SCENARIO 2 - p1 blackjacks, p2 push, dealer does not bust
        p1 = Player(Hand([Card('HJ'), Card('HA')]))
        p2 = Player(Hand([Card('HJ'), Card('C7')]))

        p1.hands[0].status = 'blackjack'
        p2.hands[0].status = 'stand'

        self.assertEqual(p1.recent_winloss, [])
        self.assertEqual(p2.recent_winloss, [])

        dealer_cards = [Card('HJ'), Card('C7')] # no bust
        Jack.resolve_hands(p1, dealer_cards)
        Jack.resolve_hands(p2, dealer_cards)

        self.assertEqual(len(p1.recent_winloss), 1)
        self.assertEqual(len(p2.recent_winloss), 1)

        self.assertEqual(p1.recent_winloss[0], 2.5)
        self.assertEqual(p2.recent_winloss[0], 1)

        # SCENARIO 3 - p1 push, p2 loses normally 
        p1 = Player(Hand([Card('H9'), Card('H9')]))
        p2 = Player(Hand([Card('H2'), Card('C3')]))

        p1.hands[0].status = 'stand'
        p2.hands[0].status = 'stand'

        self.assertEqual(p1.recent_winloss, [])
        self.assertEqual(p2.recent_winloss, [])

        dealer_cards = [Card('H9'), Card('C9')] # no bust
        Jack.resolve_hands(p1, dealer_cards)
        Jack.resolve_hands(p2, dealer_cards)

        self.assertEqual(len(p1.recent_winloss), 1)
        self.assertEqual(len(p2.recent_winloss), 1)

        self.assertEqual(p1.recent_winloss[0], 1)
        self.assertEqual(p2.recent_winloss[0], 0)

        # SCENARIO 4 - p1 blackjack push, p2 unnat blackjack (loss), dealer blackjacks
        p1 = Player(Hand([Card('HA'), Card('D10')]))
        p2 = Player(Hand([Card('H2'), Card('C3'),Card('C10'),Card('D6')]))

        p1.hands[0].status = 'blackjack'
        p2.hands[0].status = 'unnat'

        self.assertEqual(p1.recent_winloss, [])
        self.assertEqual(p2.recent_winloss, [])

        dealer_cards = [Card('HA'), Card('C10')] # no bust
        Jack.resolve_hands(p1, dealer_cards)
        Jack.resolve_hands(p2, dealer_cards)

        self.assertEqual(len(p1.recent_winloss), 1)
        self.assertEqual(len(p2.recent_winloss), 1)

        self.assertEqual(p1.recent_winloss[0], 1)
        self.assertEqual(p2.recent_winloss[0], 0)

    # assumes players in order starting at dealer's left
    # assumes dealer deals first cards to players, then self, then 
    #   second cards to players
    def test_deal_cards(self):
        h1 = Hand([]) # WARNING: not passing an arg to Hand() causes a shared mem logic err
        h2 = Hand([])
        p1              = Player(h1)
        p2              = Player(h2)
        dealer_hand     = []
        shoe            = Shoe()
        shoe.cards = [Card('D2'), Card('D3'), Card('D4'), Card('D5'), Card('D6'), Card('D7')]

        Jack.deal_cards(shoe, [p1,p2], dealer_hand)

        self.assertEqual(p1.hands[0].cards[0].name, 'D2')
        self.assertEqual(p2.hands[0].cards[0].name, 'D3')

        self.assertEqual(dealer_hand[0].name, 'D4')

        self.assertEqual(p1.hands[0].cards[1].name, 'D5')
        self.assertEqual(p2.hands[0].cards[1].name, 'D6')

        self.assertEqual(dealer_hand[1].name, 'D7')

        self.assertEqual(len(shoe.cards), 0)

    def test_game(self):
        # p1: HJ H9 stands. result: win
        # p2: DJ C3 hits, gets 4. result: loss
        # dealer: H10 H4 hits, gets 4. result: NA
        p1 = Player()
        p2 = Player()
        shoe = Shoe()
        shoe.cards = [Card('HJ'), Card('DJ'), Card('H10'), Card('H9'), Card('C3'), Card('H4'), Card('C4'), Card('D4')]
        Jack.game(shoe, [p1, p2])

        self.assertEqual(len(shoe.cards), 0)
        self.assertEqual(p1.recent_winloss, [2])
        self.assertEqual(p2.recent_winloss, [0])

        self.assertEqual(set([x.name for x in p1.hands[0].cards]), set(['HJ', 'H9']))
        self.assertEqual(set([x.name for x in p2.hands[0].cards]), set(['DJ', 'C3', 'C4']))

    def test_game_should_iterate_over_split_hands(self):
        p1 = Player() # splits to (H8 C9) (C8 C10)
        shoe = Shoe()
        shoe.cards = [Card('H8'), Card('DJ'), Card('C8'), Card('H9'), Card('C9'), Card('C10')]
        Jack.game(shoe, [p1])

        self.assertEqual(len(shoe.cards), 0)
        self.assertEqual(p1.recent_winloss, [0,0])

        self.assertEqual(set([x.name for x in p1.hands[0].cards]), set(['H8', 'C9']))
        self.assertEqual(set([x.name for x in p1.hands[1].cards]), set(['C8', 'C10']))

    def test_n_games(self):
        p1 = Player()
        p2 = Player() 
        p3 = Player()
        Jack.n_games([p1,p2,p3], 3)
        #self.assertEqual(len(p1.recent_winloss), 3) 

    def test_intg_incrementUnitSpent(self):
        # regular
        p1 = Player(Hand([Card('H10'), Card('D10')]))
        shoe = Shoe() 
        upcard = Card('S2') 
        Jack.turn(shoe, p1, 0, upcard)
        self.assertEqual(p1.units_spent, 1)

        # split 
        p1 = Player(Hand([Card('H8'), Card('D8')]))
        shoe = Shoe() 
        shoe.cards = [Card('H10'),Card('H10')]
        upcard = Card('S2')   
        self.assertEqual(p1.units_spent, 0)           
        Jack.turn(shoe, p1, 0, upcard)
        self.assertEqual(p1.units_spent, 2)

        # double down
        p1 = Player(Hand([Card('H4'), Card('H6')]))
        shoe = Shoe() 
        shoe.cards = [Card('H10'),Card('H10')]
        upcard = Card('S2')              
        Jack.turn(shoe, p1, 0, upcard)
        self.assertEqual(p1.units_spent, 2)



# if __name__ == '__main__':
#     unittest.main()


# with self.assertRaises(TypeError):



