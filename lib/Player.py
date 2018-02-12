from Hand import Hand

class Player:

    def __init__(self, hand=None):
        if hand is None:
            hand = Hand()
        self.hands = {0: hand}# initialize to one hand
        self.recent_winloss = [] # results in units from recent game
        self.units_spent = 0

    def reset(self):
        self.hands = {0: Hand()}
        self.recent_winloss = []
        self.units_spent = 0
        
    def reset_recent_winloss(self):
        self.recent_winloss = []

    # Assumes a player doesn't start out with multiple hands
    def clear_hands(self):
        self.hands = {0: Hand()}

    def update_bankroll(self):
        self.bankroll += sum(self.recent_winloss)
        self.reset_recent_winloss

    # returns key of newly created hand 
    def split(self, currentHandKey):
        num_hands = len(self.hands.keys())
        new_hand = self.hands[currentHandKey].cards.pop() #grab card from old hand
        self.hands[num_hands] = Hand([new_hand])

        return num_hands # key of new hand

    def increaseBetOfHand(self, handKey):
        self.hands[handKey].increaseBet()
        self.incrementUnitSpent()

    # currently assumes all bets are 1 unit, so this is called
    # at split and doubledown
    def incrementUnitSpent(self):
        self.units_spent += 1

    # A crude fix for the fact that split recurses
    # on turn(), which calls incrementUnitSpent
    def decrementUnitSpent(self):
        self.units_spent -= 1

