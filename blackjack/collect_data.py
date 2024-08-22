import blackjack
import csv

def get_data(trials=100):
    data = blackjack.sim_game(trials)

    with open('blackjack_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['PlayerValue', 'DealerValue', 'Result', 'InitialBalance', 'FinalBalance'])
        writer.writerows(data)