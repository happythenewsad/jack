import logging

from BasicStrategy import BasicStrategy as bs
from Card import Card
from Player import Player
from Shoe import Shoe
from Utils import Utils
from Hand import Hand


class Jack:
    @staticmethod
    def deal_cards(shoe, players, dealer_hand):
        for idx, player in enumerate(players):
            for handKey in players[idx].hands.keys(): 
                card = shoe.pop()
                players[idx].hands[handKey].cards.append(card)

        dealer_hand.append(shoe.pop())

        for player in players:
            for handKey in player.hands.keys(): 
                player.hands[handKey].cards.append(shoe.pop()) 

        dealer_hand.append(shoe.pop())       

    # input: array of Cards
    @staticmethod
    def up_to_17(shoe,dealer_hand):
        while Utils.card_value(dealer_hand) < 17:
            dealer_hand.append(shoe.pop())

    # starts a new shoe when old one is exhausted
    @staticmethod
    def n_games(players,n):
        shoe = Shoe()

        for i in range(n):
            if shoe.end_of_shoe:
                shoe = Shoe()
                logging.debug("initialized new shoe with initial cards: {0}, {1}".format( \
                    shoe.cards[0].name, shoe.cards[1].name))

            Jack.game(shoe, players)
            [x.clear_hands() for x in players]

    def play_shoe(players, shoe=None):
        if shoe is None:
            shoe = Shoe()
        while not shoe.end_of_shoe:
            Jack.game(shoe, players)
            [x.clear_hands() for x in players]        

    @staticmethod
    def game(shoe, players):
        dealer_hand = []
        Jack.deal_cards(shoe, players, dealer_hand)

        for player in players:
            for handKey in list(player.hands.keys()):
                Jack.turn(shoe, player, handKey, dealer_hand[0])

        Jack.up_to_17(shoe,dealer_hand)

        for player in players:        
            Jack.resolve_hands(player, dealer_hand)

        # TODO: update bankroll here?

    # player can have multiple hands bc of split
    # final money can be computed from initial money
    def resolve_hands(player, dealer_cards):

        for handKey in player.hands.keys():
            hand = player.hands[handKey]

            if hand.surrendered():
                result = hand.units / 2
            elif hand.busted():
                result = 0
            elif Utils.isBlackjack(dealer_cards):
                if hand.blackjack():
                    result = hand.units 
                else:
                    result = 0
            elif hand.blackjack(): 
                result = hand.units * 2.5  # TODO: make default config
            elif Utils.busted(dealer_cards):
                result = hand.units * 2
            elif Utils.card_value(hand.cards) == Utils.card_value(dealer_cards):
                result = hand.units
            elif Utils.card_value(hand.cards) < Utils.card_value(dealer_cards):
                result = 0
            elif Utils.card_value(hand.cards) > Utils.card_value(dealer_cards):
                result = hand.units * 2
            else:
                raise ValueError("resolve_hands: Unhandled case!")

            #logging.warning("Hand {0} with {1} against {2} result: {3}".format(handKey, hand.pretty(), [x.name for x in dealer_cards], result))
            player.recent_winloss.append(result)


    # playerHand: index of the player's hand (can be > 1 if split occured)
    # TODO: change to not have return statement. operate on hand objs only
    def turn(shoe, player, playerHandKey, upcard, initialHand=True):
        proceed = True
        result = None # blackjack, busted, or value
        player.incrementUnitSpent()

        hand = player.hands[playerHandKey]
        cards = hand.cards 
        col = bs.lookup_upcard_idx(upcard)

        while proceed: 

            if Utils.busted(cards):
                hand.status = 'busted'
                return 
            if Utils.card_value(cards) == 21: 
                bj_or_unnat = 'blackjack' if initialHand else 'unnat'
                hand.status = bj_or_unnat
                return 

            if (len(cards)) == 2 and Jack.has_double(cards): # use split decision matrix
                row = bs.lookup_split_row(cards)
                result = bs.pairs_decision[row][col]
            elif (len(cards) == 1): # turn after split
                result = 'hit'
            elif Utils.has_soft_total(cards): # has soft total
                row = bs.lookup_soft_row(cards) 
                result = bs.soft_decision[row][col]
            else: #regular matrix
                row = bs.lookup_normal_row(cards)
                result = bs.decision[row][col]

            hand.status = result

            if result == 'sur': 
                if not initialHand:
                    hand.status = 'hit'
                return 

            if result == 'stand':
                return 
            elif result == 'hit':
                proceed = True
                hand.cards.append(shoe.pop()) 
            elif result == 'ddown':
                if initialHand:
                    proceed = False
                    player.increaseBetOfHand(playerHandKey)
                else: #hit
                    proceed = True
                    hand.status = 'hit'
                hand.cards.append(shoe.pop())
            elif result == 'ddownS':
                if initialHand:
                    proceed = False
                    player.increaseBetOfHand(playerHandKey)
                else: #stand
                    proceed = False
                    hand.status = 'stand'
                hand.cards.append(shoe.pop())
            elif result == 'split': # split
                player.decrementUnitSpent() #because of recursive turn()
                newHandKey = player.split(playerHandKey)
                outcome1, outcome2 = Jack.turn(shoe, player, playerHandKey, upcard, False), Jack.turn(shoe, player, newHandKey, upcard, False)
            else:
                raise ValueError("turn: unhandled value {0} with player cards: {1} upcard: {2}".format(result, [x.name for x in cards], upcard.name))

            initialHand = False

        if result == None:
            raise ValueError("turn: result value is None")


    # assumes input cardinality is exactly 2
    def has_double(cards):
        if len(cards) != 2:
            raise ValueError("has_double: card number is {0}".format(len(cards)))

        return cards[0].name[1:] == cards[1].name[1:]
