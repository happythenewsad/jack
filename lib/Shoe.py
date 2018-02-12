from Card import Card
import random as rd
import logging

class Shoe:
    @staticmethod
    def gen_cards(num_decks):
        card_list = list(Card.card_values.keys())
        cards = []
        for i in range(num_decks):
            cards.extend([Card(c) for c in card_list])
        rd.shuffle(cards)
        return cards

    # returns false if at least one removal was unsuccessful
    def removeCards(self, val_set, n): 
        for i in range(n):
            found_card = False
            for idx,card in enumerate(self.cards):
                if card.value in val_set:
                    self.cards.pop(idx)
                    found_card = True
                    break

            if not found_card:
                return False 
        return True


    def __init__(self, decks=8):
        self.cards = Shoe.gen_cards(decks)
        self.end_of_shoe = False

    def pop(self):
        if len(self.cards) <= 0:
            self.cards.append(Shoe.gen_cards(1).pop())
            self.end_of_shoe = True
        return self.cards.pop(0)
