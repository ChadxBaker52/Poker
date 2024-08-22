import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random import choice
from deck_of_cards import Deck, Hand

class Balance:
    def __init__(self, balance):
        self.balance = balance
    
    def bet(self, amount, type):
        self.balance -= amount
        
    def win(self, amount, type):
        self.balance += (2*amount)
        
    def tie(self, amount, type):
        self.balance += amount

def count_cards(count, card):
    if card.get_val() <= 6:
        count += 1
    elif card.get_val() > 9:
        count -= 1
    return count

def make_decision(player_value, dealer_value, card_count):
    if player_value >= 17:
        return 0
    elif player_value >= 13:
        if dealer_value >= 7:
            return 1
        else:
            return 0
    elif player_value == 12:
        if dealer_value == 2 or dealer_value == 3 or dealer_value >= 7:
            return 1
        else:
            return 0
    else:
        return 1
        
def sim_game(trials=1, num_of_decks=2):
    deck = Deck(num_of_decks)
    
    balance = Balance(10000)
    bet = 10
    game_data = []
    card_count = 0
    
    for _ in range(trials):
        if card_count > 7:
            bet = 50
        elif card_count > 4:
            bet = 25
        else:
            bet = 15
        
        initial_balance = balance.balance
        balance.bet(bet)
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.get_card(deck)
        dealer_hand.get_card(deck)
        player_hand.get_card(deck)
        dealer_hand.get_card(deck)
        
        card_count = count_cards(card_count, player_hand.cards[0])
        card_count = count_cards(card_count, player_hand.cards[1])
        card_count = count_cards(card_count, dealer_hand.cards[0])
        card_count = count_cards(card_count, dealer_hand.cards[1])
        
        result = ''
        #options = ['hit', 'hit', 'hit', 'stand', 'stand']
        
        if player_hand.get_value() == 21:
            if dealer_hand.get_value() == 21:
                balance.tie(bet)
                result = 't'
            else:
                balance.win(bet)
                result = 'w'
        else:
            while player_hand.get_value() < 21:
                action = make_decision(player_hand.get_value(), dealer_hand.get_value(flipped=True), card_count)
                if action == 1:
                    player_hand.get_card(deck)
                else:
                    break
                
            while dealer_hand.get_value() < 17:
                dealer_hand.get_card(deck)
                
            if player_hand.get_value() <= 21:
                if dealer_hand.get_value() > 21 or player_hand.get_value() > dealer_hand.get_value():
                    balance.win(bet)
                    result = 'w'
                elif player_hand.get_value() == dealer_hand.get_value():
                    balance.tie(bet)
                    result = 't'
                else:
                    result = "l"
                    
                if balance.balance < 0:
                    break
            else:
                result = "l"
            
        final_balance = balance.balance
        game_data.append((player_hand.get_value(), dealer_hand.get_value(flipped=True), result, initial_balance, final_balance))
    
    return game_data

sim_game(10)
    