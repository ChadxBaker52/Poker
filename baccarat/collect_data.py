import baccarat
import csv

def data_sim(trials=1, num_of_losses=10, max_balance=130):
    data = baccarat.sim_game(trials, num_of_losses, max_balance)

    with open('baccarat_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['PlayerValue', 'DealerValue', 'BetAmount', 'BetType', 'Result', 'InitialBalance', 'FinalBalance'])
        writer.writerows(data)