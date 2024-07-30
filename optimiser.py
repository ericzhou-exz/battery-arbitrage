import pandas as pd
import numpy as np
import pyomo
import matplotlib.pyplot as plt

# Step 1: Load the Data
folders = ['nsw', 'vic', 'qld', 'sa', 'tas']

# Step 2: Define Battery Parameters
capacity = 1  # Battery capacity in MWh
power_rating = 1  # Maximum charge rate in MW
efficiency = 0.9  # Round-trip efficiency
soc = 0.5

sell = 2000
buy = 200

#sell_arr = pd.Series(prices).rolling(1000).quantile(0.9, interpolation='linear')
#buy_arr =  pd.Series(prices).rolling(1000).quantile(0.1, interpolation='linear')
#print(sell_arr)
# cost is 14400 per 5 kW / 10 kWh

#for sell in [100, 200, 500, 1000, 2000, 5000, 10000]:
#    for buy in [0, 10, 20, 50, 100, 200, 500, 1000, 2000]:
#for capacity in [1, 2, 4, 8, 16]:

for folder in folders:
    data = pd.read_csv(f'{folder}/concatenated_output.csv')
    prices = data['RRP'].values
    demand = data['TOTALDEMAND'].values

    total_charge_cost = 0
    total_discharge_revenue = 0
    battery_dispatch = []
    soc_list = []

    for i, price in enumerate(prices):
        #sell = np.quantile(prices[i:i+100], 0.75)
        #buy = np.quantile(prices[i:i+100], 0.25)
        #sell = sell_arr[i]
        #buy = buy_arr[i]

        if price < buy and soc < 0.9:
            total_charge_cost += price / 12
            soc += (power_rating / capacity) / 12
            battery_dispatch.append(-power_rating)

        elif price > sell and soc > 0.1:
            total_discharge_revenue += price / 12
            soc -= (power_rating / capacity) / 12
            battery_dispatch.append(power_rating)

        else:
            battery_dispatch.append(0)
        
        soc_list.append(soc)

    utilisation = np.count_nonzero(battery_dispatch) / len(prices)
    profit = total_discharge_revenue - total_charge_cost
    print(profit, sell, buy, capacity, utilisation)

    residual_demand = [a - b for a, b in zip(demand, battery_dispatch)]
    #plt.plot(battery_dispatch)
    #plt.plot(demand)
    #plt.plot(residual_demand)
    #plt.show()

    avg_demand = [0] * 288
    avg_battery = [0] * 288
    avg_residual = [0] * 288
    avg_prices = [0] * 288
    avg_soc = [0] * 288

    for i in range(288):
        for j in range(365):
            avg_demand[i] += demand[j*288 + i] / 365
            avg_battery[i] += battery_dispatch[j*288 + i] / 365
            avg_residual[i] += residual_demand[j*288 + i] / 365
            avg_prices[i] += prices[j*288 + i] / 365
            avg_soc[i] += 1000 * soc_list[j*288 + i] / 365

    plt.plot(avg_demand)
    plt.plot(avg_battery)
    plt.plot(avg_residual)
    plt.plot(avg_prices)
    plt.plot(avg_soc)
    plt.ylabel('Demand (MW)')
    plt.xlabel('Time of day')
    plt.title(folder)
    plt.show()