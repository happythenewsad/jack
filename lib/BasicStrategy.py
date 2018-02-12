import numpy as np
from Utils import Utils

#Assumptions:
    # can double on anything

# ddownS means stand if not allowed to double down
# ddown means hit if not allowed to double down
class BasicStrategy:
    # actions: Stand Hit sPlit suRrender

    # regular decision matrix ########################
    decision                = np.full((9,10),'hit', dtype=object)
    decision[0]             = 'stand' 
    decision[1][0:5]        = 'stand'
    decision[2][0:5]        = 'stand'
    decision[3][0:5]        = 'stand'
    decision[4][2:5]        = 'stand'

    decision[1][7:]         = 'sur'
    decision[2][8]          = 'sur'

    decision[5]             = 'ddown'
    decision[6][0:8]        = 'ddown'
    decision[7][1:5]        = 'ddown'

    # pairs decision matrix ########################
    pairs_decision          = np.full((9,10), 'split', dtype=object)
    pairs_decision[1]       = 'stand'
    pairs_decision[2][5]    = 'stand'
    pairs_decision[2][5]    = 'stand'
    pairs_decision[2][8:]   = 'stand'

    pairs_decision[4][6:]   = 'hit'
    pairs_decision[5][5:]   = 'hit'
    pairs_decision[6][8:]   = 'hit'
    pairs_decision[7][0:3]  = 'hit'
    pairs_decision[7][5:]   = 'hit'
    pairs_decision[8][6:]   = 'hit'

    pairs_decision[6][0:8]  = 'ddown'

    # soft decision matrix ########################
    soft_decision           = np.full((6,10), 'hit', dtype=object)
    soft_decision[0]        = 'stand'
    soft_decision[1]        = 'stand'
    soft_decision[2][5:7]   = 'stand'

    soft_decision[1][4]     = 'ddownS'
    soft_decision[2][0:5]   = 'ddownS'
    soft_decision[3][1:5]   = 'ddown'
    soft_decision[4][2:5]   = 'ddown'
    soft_decision[5][3:5]   = 'ddown'

    @classmethod
    def printStrategy(self):
        print("Regular: \n{0}\n Pairs: \n{1}\n".format(self.decision, self.pairs_decision))


    def lookup_soft_row(cards):
        card_val = Utils.card_value(cards) # must be 9 or below, otherwise BJ/bust
        if card_val > 20:
            raise ValueError("lookup_soft_row: Card value greater than 20: ", card_val)

        if card_val == 15 or card_val == 16:
            return 4
        if card_val == 13 or card_val == 14:
            return 5

        return 20 - card_val


    def lookup_split_row(cards):
        single_value = cards[0].value # arbitrarily pick first card
        if single_value == 11: #ace
            return 0
        if single_value == 2:
            return 8

        return 10 - single_value + 1


    def lookup_normal_row(cards):
        total_value = Utils.card_value(cards)

        if total_value >= 17:
            return 0
        elif total_value <= 8:
            return 8
        elif total_value == 16:
            return 1
        elif total_value == 15:
            return 2
        elif total_value >= 13 and total_value <= 14:
            return 3
        elif total_value == 12:
            return 4
        elif total_value == 11:
            return 5
        elif total_value == 10:  
            return 6
        elif total_value == 9:
            return 7
        else: 
            raise ValueError("Invalid input")

    # indexes for columns, i.e. upcard
    def lookup_upcard_idx(card):
        if Utils.has_ace([card]):
            return 9
        elif card.value >= 2 and card.value <= 10:
            return card.value -2
        else:
            raise ValueError("Invalid input")

