import pandas as pd
import numpy as np
import pyomo
import matplotlib

# Step 1: Load the Data
data = pd.read_csv('nsw/concatenated_output.csv')
prices = data['RRP'].values

# Step 2: Define Battery Parameters
capacity = 1  # Battery capacity in MWh
max_charge_rate = 1  # Maximum charge rate in MW
max_discharge_rate = 1  # Maximum discharge rate in MW
efficiency = 0.9  # Round-trip efficiency
soc = 0.5

#sell = 200
#buy = 50

sell_arr = pd.Series(prices).rolling(1000).quantile(0.9, interpolation='linear')
buy_arr =  pd.Series(prices).rolling(1000).quantile(0.1, interpolation='linear')
#print(sell_arr)

#for sell in [100, 200, 500, 1000, 2000, 5000, 10000]:
#    for buy in [0, 10, 20, 50, 100, 200, 500, 1000, 2000]:
for capacity in [1, 2, 4, 8, 16]:
    total_charge_cost = 0
    total_discharge_revenue = 0
    charge_status = []

    for i, price in enumerate(prices):
        #sell = np.quantile(prices[i:i+100], 0.75)
        #buy = np.quantile(prices[i:i+100], 0.25)
        sell = sell_arr[i]
        buy = buy_arr[i]

        if price > sell and soc > 0.1:
            total_discharge_revenue += price / 12
            soc -= (max_discharge_rate / capacity) / 12
            charge_status.append(1)

        elif price < buy and soc < 0.9:
            total_charge_cost += price / 12
            soc += (max_charge_rate / capacity) / 12
            charge_status.append(-1)

        else:
            charge_status.append(0)

    utilisation = np.count_nonzero(charge_status) / len(prices)
    profit = total_discharge_revenue - total_charge_cost
    print(profit, sell, buy, capacity, utilisation)