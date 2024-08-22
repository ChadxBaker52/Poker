import pandas as pd
import collect_data
from statistics import mean

def chance_of_profit(trials, num_of_losses=10, max_balance=130, dfs=100):
    winners = 0
    for _ in range(dfs):
        collect_data.data_sim(trials, num_of_losses, max_balance)
        df = pd.read_csv('baccarat_data.csv')
        balance = df['FinalBalance']
        if balance.iloc[-1] > 99:
            winners += 1
    return winners/dfs
    
# per = chance_of_profit(30)
# print(per)

def grid_search(loss_range, balance_range, trials=100):
    best_success_rate = 0
    best_params = None
    for num_of_losses in loss_range:
        for max_balance in balance_range:
            success_rate = chance_of_profit(trials, num_of_losses, max_balance)
            if success_rate > best_success_rate:
                best_success_rate = success_rate
                best_params = (num_of_losses, max_balance)
    
    return best_params, best_success_rate

loss_range = range(2, 15)  # Example range for num_of_losses
balance_range = range(125, 200, 5)  # Example range for max_balance

best_params, best_success_rate = grid_search(loss_range, balance_range, trials=100)
print(f'Best Parameters: num_of_losses={best_params[0]}, max_balance={best_params[1]}')
print(f'Highest Success Rate: {best_success_rate:.2%}')
