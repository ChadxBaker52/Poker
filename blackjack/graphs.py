import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collect_data import get_data

get_data(10000000)
df = pd.read_csv('blackjack_data.csv')

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

# heatmap(df)

def balance_graph(df):
    # Assuming 'GameNumber' is a column that represents the order of the games
    # If not, create it based on the index
    if 'GameNumber' not in df.columns:
        df['GameNumber'] = df.index + 1

    # Extract relevant columns
    game_numbers = df['GameNumber']
    balances = df['FinalBalance']

    # Plot the balance over time
    plt.figure(figsize=(10, 6))
    plt.plot(game_numbers, balances, marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.title('Balance Over Time')
    plt.xlabel('Game Number')
    plt.ylabel('Balance')
    plt.grid(True)

    # Show the plot
    plt.show()
    
# balance_graph(df)

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
    
data_out(df)