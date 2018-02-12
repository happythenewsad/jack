# belongs to: Player
class Hand:
    def __init__(self, cards=None, units=1):
        if cards is None:
            cards = []
        self.cards = cards
        self.units = units
        self.status = None # stand sur ddown busted blackjack unnat

    def increaseBet(self):
        self.units += 1

    def busted(self):
        return self.status == 'busted'

    def surrendered(self):
        return self.status == 'sur'

    # natural blackjack
    def blackjack(self):
        return self.status == 'blackjack'

    def pretty(self):
        return [x.name for x in self.cards]




