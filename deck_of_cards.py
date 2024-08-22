from random import shuffle, uniform

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def get_val(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11
        else:
            return int(self.rank)
        
    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"
    
    def get_image_path(self):
        return f"cards/{self.rank.lower()}_of_{self.suit.lower()}.png"
    
class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ['2','3','4','5','6','7','8','9','10','Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards = [Card(suit, rank) for suit in Deck.suits for rank in Deck.ranks] * num_decks
        self.shuffle()
        num_cards = 52 * num_decks
        cut_card = uniform((num_cards*0.2), (num_cards*0.4))
        self.cards.insert(int(cut_card), "cut")
        
    def shuffle(self):
        shuffle(self.cards)
        
    def deal_card(self):
        card = self.cards.pop()
        if card == "cut":
            self.reset()
            card = self.cards.pop()
        return card
    
    def reset(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks] * self.num_decks
        self.shuffle()
        num_cards = 52 * self.num_decks
        cut_card = uniform((num_cards * 0.3), (num_cards * 0.4))
        self.cards.insert(int(cut_card), "cut")
        
    def print_deck(self):
        i = 1
        for card in self.cards:
            print(card, i)
            i += 1

class Hand:
    def __init__(self, flipped=False):
        self.cards = []
        self.flipped = flipped
        
    def get_card(self, deck):
        card = deck.deal_card()
        self.cards.append(card)
        
    # def get_value(self):
    #     value = sum(0 if card.rank in ['Jack', 'Queen', 'King'] else (1 if card.rank == 'Ace' else int(card.rank)) for card in self.cards)
    #     return value % 10 
            
    def get_value(self, flipped=False):
        # values = {'1':21, '2':2, '3':3, '4':4 ,'5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
        value = 0
        num_aces = 0
        if flipped:
            card = self.cards[0]
            if card.rank in ['Jack', 'Queen', 'King']:
                return 10
            elif card.rank == 'Ace':
                return 11
            else:
                return int(card.rank)
        else:
            for card in self.cards:
                if card.rank in ['Jack', 'Queen', 'King']:
                    value += 10
                elif card.rank == 'Ace':
                    num_aces += 1
                    value += 11
                else:
                    value += int(card.rank)

            while value > 21 and num_aces:
                value -= 10
                num_aces -= 1

        return value