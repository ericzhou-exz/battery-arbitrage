import pandas as pd
import numpy as np
import pyomo

# Step 1: Load the Data
data = pd.read_csv('nsw/concatenated_output.csv')
prices = data['RRP'].values

# Step 2: Define Battery Parameters
capacity = 1  # Battery capacity in MWh
max_charge_rate = 1  # Maximum charge rate in MW
max_discharge_rate = 1  # Maximum discharge rate in MW
efficiency = 0.9  # Round-trip efficiency
soc = 0.5

total_charge_cost = 0
total_discharge_revenue = 0

charge_status = []

sell = 5000
buy = 30

for i, price in enumerate(prices):
    if price > sell and soc > 0.1:
        total_discharge_revenue += price / 12
        soc -= (max_discharge_rate / capacity) / 12
        charge_status.append(1)
        print(f'{price} discharge {soc}')
    elif price < buy and soc < 0.9:
        total_charge_cost += price / 12
        soc += (max_charge_rate / capacity) / 12
        charge_status.append(-1)
        #print(f'{price} charge')
    else:
        charge_status.append(0)
        #print(f'{price} hold')

profit = total_discharge_revenue - total_charge_cost
print(sell, buy, profit)
print(prices.mean())