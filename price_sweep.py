import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn

folders = ['nsw', 'qld', 'sa', 'tas', 'vic']

# Step 2: Define Battery Parameters
duration = 2  # Battery capacity in MWh
#power_rating = 300  # Maximum charge rate in MW
soc = 0.5

def run_battery(buy, sell):
    total_charge_cost = 0
    total_discharge_revenue = 0
    soc = 0.5

    for i, price in enumerate(prices):
        if price < buy and soc < 0.9:
            total_charge_cost += price / 12
            soc += (1 / duration) / 12

        elif price > sell and soc > 0.1:
            total_discharge_revenue += price / 12
            soc -= (1 / duration) / 12

    profit = total_discharge_revenue - total_charge_cost
    #print(profit, sell, buy)
    return profit

for folder in folders:
    data = pd.read_csv(f'{folder}/concatenated_output.csv')
    prices = data['RRP'].values
    demand = data['TOTALDEMAND'].values
    
    clipped_prices = np.clip(prices, -50, 200)
    plt.hist(clipped_prices, bins=20)
    plt.title(f'{folder.upper()} price histogram')
    plt.xlabel('Price ($)')
    plt.ylabel('Percentage of intervals')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(12*24*365))
    plt.tight_layout()
    plt.savefig(f'figs/{folder} price histogram')
    plt.clf()

for folder in folders:
    data = pd.read_csv(f'{folder}/concatenated_output.csv')
    prices = data['RRP'].values
    demand = data['TOTALDEMAND'].values

    total_charge_cost = 0
    total_discharge_revenue = 0
    battery_dispatch = []
    soc_list = []

    #profit_results = np.zeros((20, 20))
    sell_arr = np.arange(-100, 1000, 50)
    buy_arr = np.arange(-100, 1000, 50)

    # Create a meshgrid
    X, Y = np.meshgrid(sell_arr, buy_arr)
    profit_results = np.array([[run_battery(x, y) for x in sell_arr] for y in buy_arr])
    
    # Create a heatmap
    #plt.matshow(profit_results)
    #plt.figure(figsize=(8, 6))
    seaborn.heatmap(profit_results, xticklabels=np.round(sell_arr, 2), yticklabels=np.round(buy_arr, 2), cmap='vlag')

    # Add titles and labels
    plt.title(f'{folder.upper()} arbitrage profit')
    plt.xlabel('Sell price ($)')
    plt.ylabel('Buy price ($)')

    # Show the plot
    plt.tight_layout()
    plt.savefig(f'figs/{folder} price sweep')
    plt.clf()