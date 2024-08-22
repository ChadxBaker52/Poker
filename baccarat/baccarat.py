import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deck_of_cards import Card, Hand, Deck, Balance
from random import choice

def sim_game(trials=1, num_of_losses=3, max_balance=150):
    deck = Deck(num_decks=8)
    
    balance = Balance(100)
    result = ''
    bet_type = 'd'
    bet = 50
    
    game_data = []
    
    for _ in range(trials):
        initial_balance = balance.balance
        balance.bet(bet)
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.get_card(deck)
        # print("First player card dealt:", player_hand.cards[0])
        dealer_hand.get_card(deck)
        # print("First dealer card dealt:", dealer_hand.cards[0])
        player_hand.get_card(deck)
        # print("Second player card dealt:", player_hand.cards[1])
        dealer_hand.get_card(deck)
        # print("Second dealer card dealt:", dealer_hand.cards[1])
        
        player_value = player_hand.get_value()
        # print("Player value:", player_value)
        dealer_value = dealer_hand.get_value()
        # print("Dealer value:", dealer_value)
        
        player_natural = player_value == 8 or player_value == 9
        # print("Player Natural:", player_natural)
        dealer_natural = dealer_value == 8 or dealer_value == 9
        # print("Dealer Natural:", dealer_natural)
        
        if not (player_natural or dealer_natural):
            third_card = False
            third_card_val = 50
            if player_value <= 5:
                player_hand.get_card(deck)
                third_card = True
                # print("Player got third card:", player_hand.cards[2])
                if player_hand.cards[2].rank in ['Jack', 'Queen', 'King']:
                    third_card_val = 0
                elif player_hand.cards[2].rank == 'Ace':
                    third_card_val = 1
                else:
                    third_card_val = int(player_hand.cards[2].rank)
                
            if third_card:
                if dealer_value <= 2:
                    dealer_hand.get_card(deck)
                    # print("Dealer got third card:", dealer_hand.cards[2]) 
                elif dealer_value == 3:
                    if third_card_val != 8:  
                        dealer_hand.get_card(deck)
                        # print("Dealer got third card:", dealer_hand.cards[2]) 
                elif dealer_value == 4:
                    if third_card_val >= 2 and third_card_val <= 7:
                        dealer_hand.get_card(deck)
                        # print("Dealer got third card:", dealer_hand.cards[2]) 
                elif dealer_value == 5:
                    if third_card_val >= 4 and third_card_val <= 7:
                        dealer_hand.get_card(deck)
                        # print("Dealer got third card:", dealer_hand.cards[2]) 
                elif dealer_value == 6:
                    if third_card_val >= 6 and third_card_val <= 7:
                        dealer_hand.get_card(deck)
                        # print("Dealer got third card:", dealer_hand.cards[2]) 
            else:
                if dealer_value <= 5:
                    dealer_hand.get_card(deck)
                    
        player_value = player_hand.get_value()
        # print("Player value:", player_value)
        dealer_value = dealer_hand.get_value()
        # print("Dealer value:", dealer_value)
        
        loss_count = 0
        
        if player_value > dealer_value:
            # print("Player win")
            if bet_type == 'p':
                balance.win(bet)
                bet = 10
            else:
                bet = min(bet*2, balance.balance/2)
                loss_count += 1
            result = 'w'
            
            # bet_type = 'p'
        elif player_value == dealer_value:
            # print("Tie")
            if bet_type == 't':
                balance.tie(bet*9)
                bet = bet*2
            else:
                balance.tie(bet)
            result = 't'
        else:
            # print("Lose")
            if bet_type == 'd':
                balance.win(bet*0.95)
                bet = 10
            else:
                bet = min(bet*2, balance.balance/2)
                loss_count += 1
            result = 'l'
            
            # bet_type = 'd'
            
        final_balance = balance.balance
        
        # 'PlayerValue', 'DealerValue', 'BetAmount', 'BetType', 'Result', 'InitialBalance', 'FinalBalance'
        game_data.append((player_value, dealer_value, bet, bet_type, result, initial_balance, final_balance))
        
        if final_balance <= 0:
            break
        
        if loss_count >= 6:
            bet = 10
            loss_count = 0
        
    return game_data