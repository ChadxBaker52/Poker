import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import collect_data
from statistics import mean

# Load the data
# df = pd.read_csv('baccarat_data.csv')
def dfs(num=5):
    if num == 1:
        df = pd.read_csv('baccarat_data.csv')
        return df
    else:
        dfs = []
        for _ in range(num):
            collect_data.data_sim(100, 10, 130)
            df = pd.read_csv('baccarat_data.csv')
            dfs.append(df)
        return dfs

def heatmap(df):
    # Calculate counts and win counts for each combination of PlayerValue and DealerValue
    counts = df.groupby(['PlayerValue', 'DealerValue']).size().reset_index(name='Counts')
    win_counts = df[df['Result'] == 'w'].groupby(['PlayerValue', 'DealerValue']).size().reset_index(name='WinCounts')

    # Merge counts and win counts
    combined = pd.merge(counts, win_counts, on=['PlayerValue', 'DealerValue'], how='left').fillna(0)

    # Apply Laplace smoothing
    combined['WinProbability'] = (combined['WinCounts'] + 1) / (combined['Counts'] + 2)

    # Pivot the data for heatmap
    win_prob_pivot = combined.pivot(index='PlayerValue', columns='DealerValue', values='WinProbability')
    win_prob_pivot.fillna(0, inplace=True)  # Fill NaNs with 0 for visualization

    # Create a heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(win_prob_pivot, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Win Probability'})
    plt.title('Player Hand Value vs Dealer Hand Value: Win Probability')
    plt.xlabel('Dealer Hand Value')
    plt.ylabel('Player Hand Value')
    plt.show()

# heatmap(dfs(1))

def balance_graph(dfs):
    # Assuming 'GameNumber' is a column that represents the order of the games
    # If not, create it based on the index
    plt.figure(figsize=(10, 6))
    
    for df in dfs:
        if 'GameNumber' not in df.columns:
            df['GameNumber'] = df.index + 1

        # Extract relevant columns
        game_numbers = df['GameNumber']
        balances = df['FinalBalance']

        # Plot the balance over time
        plt.plot(game_numbers, balances, marker='', linestyle='-')

    # Add labels and title
    plt.title('Balance Over Time')
    plt.xlabel('Game Number')
    plt.ylabel('Balance')
    plt.grid(True)

    # Show the plot
    plt.show()
    
balance_graph(dfs(10))

def chance_of_profit(trials, num_of_losses, max_balance):
    dfs = []
    for _ in range(100):
        collect_data.data_sim(trials, num_of_losses, max_balance)
        df = pd.read_csv('baccarat_data.csv')
        dfs.append(df)
    # active_dfs = len(dfs)
    winners = len(dfs)
    total_dfs = len(dfs)
    for df in dfs:
        # if 'GameNumber' not in df.columns:
        #     df['GameNumber'] = df.index + 1

        # Extract relevant columns
        # game_number = df['GameNumber']
        balance = df['FinalBalance']
        
        # if len(game_number) != trials and balance.iloc[-1] < 150:
        #     active_dfs -= 1
        if balance.iloc[-1] < 100:
            winners -= 1
        
    # print(f'Chance of not dying: {active_dfs/total_dfs}')
    # print(f'Won money: {winners/total_dfs}')
    return winners/total_dfs

# data = []
# for _ in range(100):
#     per = chance_of_working(dfs(100), 30)
#     data.append(per)
# print(mean(data))

def win_vs_loss_graph(dfs):
    plt.figure(figsize=(10,6))
    
    for df in dfs:
        if 'GameNumber' not in df.columns:
            df['GameNumber'] = df.index + 1
        df['CumulativeWins'] = df['Result'].eq('w').cumsum()
        plt.plot(df['GameNumber'], df['CumulativeWins'], marker='', linestyle='-')
        
    plt.title('Player Wins')
    plt.xlabel('Game Number')
    plt.ylabel('Wins')
    plt.xlim(0, 10000)
    plt.ylim(0, 10000)
    plt.axhline(y=5000, color='red', linestyle='--', linewidth=1)
    plt.grid(True)
    
    plt.show()
    
# win_vs_loss_graph(dfs(10))

def data_out(df):
    wins = df['Result'].eq('w').sum()
    losses = df['Result'].eq('l').sum()
    ties = df['Result'].eq('t').sum()
    total = len(df['Result'])
    
    win_percentage = (wins / total) * 100
    loss_percentage = (losses / total) * 100
    tie_percentage = (ties / total) * 100
    
    # Print results
    print(f'Wins: {win_percentage:.2f}%')
    print(f'Loss: {loss_percentage:.2f}%')
    print(f'Tie: {tie_percentage:.2f}%')
    
# data_out(dfs(1))