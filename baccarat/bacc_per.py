import random

def draw_card():
    """Draw a card and return its Baccarat value."""
    card = random.randint(1, 13)
    return min(card, 10) % 10  # Cards 10, J, Q, K are worth 0

def calculate_hand(cards):
    """Calculate the hand value in Baccarat."""
    return sum(cards) % 10

def player_draws(player_hand):
    """Determine if the player draws a third card based on Baccarat rules."""
    return calculate_hand(player_hand) < 6

def banker_draws(banker_hand, player_third_card=None):
    """Determine if the banker draws a third card based on Baccarat rules."""
    banker_value = calculate_hand(banker_hand)
    
    # Banker's rules for drawing the third card
    if banker_value <= 2:
        return True
    elif banker_value == 3:
        return player_third_card is None or player_third_card != 8
    elif banker_value == 4:
        return player_third_card is not None and 2 <= player_third_card <= 7
    elif banker_value == 5:
        return player_third_card is not None and 4 <= player_third_card <= 7
    elif banker_value == 6:
        return player_third_card is not None and player_third_card in [6, 7]
    else:
        return False

def simulate_baccarat_round():
    player_hand = [draw_card(), draw_card()]
    banker_hand = [draw_card(), draw_card()]
    
    # Determine if the player draws a third card
    player_third_card = None
    if player_draws(player_hand):
        player_third_card = draw_card()
        player_hand.append(player_third_card)
    
    # Determine if the banker draws a third card
    if banker_draws(banker_hand, player_third_card):
        banker_hand.append(draw_card())
    
    # Calculate the final hand values
    player_final = calculate_hand(player_hand)
    banker_final = calculate_hand(banker_hand)
    
    # Determine the outcome
    if player_final > banker_final:
        return "Player"
    elif banker_final > player_final:
        return "Banker"
    else:
        return "Tie"

def simulate_baccarat_games(num_games):
    results = {"Player": 0, "Banker": 0, "Tie": 0}
    
    for _ in range(num_games):
        outcome = simulate_baccarat_round()
        results[outcome] += 1
    
    # Calculate percentages
    player_win_percentage = (results["Player"] / num_games) * 100
    banker_win_percentage = (results["Banker"] / num_games) * 100
    tie_percentage = (results["Tie"] / num_games) * 100
    
    return {
        "Player Win %": player_win_percentage,
        "Banker Win %": banker_win_percentage,
        "Tie %": tie_percentage
    }

# Example usage
results = simulate_baccarat_games(1000000)
print(f"Player Win %: {results['Player Win %']:.2f}")
print(f"Banker Win %: {results['Banker Win %']:.2f}")
print(f"Tie %: {results['Tie %']:.2f}")
