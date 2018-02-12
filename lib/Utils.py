class Utils:
    @staticmethod
    def has_ace(cards):
        for card in cards:
            if card.name[1] == 'A':
                return True
        return False

    # this works because Ace's default value is 11
    # has valid total where ace can be either value 
    @staticmethod
    def has_soft_total(cards): 
        return Utils.has_ace(cards) and sum([c.value for c in cards]) <= 21
        # card total < indiviual total
        # A 10 5 -> 16 or 26

    # accounts for parallel value of aces
    @staticmethod
    def card_value(cards):
        value = sum([card.value for card in cards])
        for i in range(Utils.numAces(cards)):
            if value > 21:
                value = value - 10
        return value

    @staticmethod
    def isBlackjack(cards):
        return len(cards) == 2 and Utils.card_value(cards) == 21

    @staticmethod
    def busted(cards):
        return Utils.card_value(cards) > 21

    @staticmethod
    def numAces(cards):
        return sum([1 for c in cards if Utils.has_ace([c])])


