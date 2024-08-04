import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the Data
folders = ['nsw', 'qld', 'sa', 'tas', 'vic']
capacity_arr = [282, 151, 188, 17, 284]
buy_arr = [200, 50, 2000, 50, 20]
sell_arr = [200, 200, 2000, 100, 100]

# Step 2: Define Battery Parameters
duration = 2  # Battery capacity in MWh
#power_rating = 300  # Maximum charge rate in MW
soc = 0.5

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

for folder, capacity, buy, sell in zip(folders, capacity_arr, buy_arr, sell_arr):
    data = pd.read_csv(f'{folder}/concatenated_output.csv')
    prices = data['RRP'].values
    demand = data['TOTALDEMAND'].values

    total_charge_cost = 0
    total_discharge_revenue = 0
    battery_dispatch = []
    soc_list = []

    for i, price in enumerate(prices):
        if price < buy and soc < 0.9:
            total_charge_cost += price / 12
            soc += (1 / duration) / 12
            battery_dispatch.append(-capacity)

        elif price > sell and soc > 0.1:
            total_discharge_revenue += price / 12
            soc -= (1 / duration) / 12
            battery_dispatch.append(capacity)

        else:
            battery_dispatch.append(0)
        soc_list.append(soc)

    utilisation = np.count_nonzero(battery_dispatch) / len(prices)
    profit = total_discharge_revenue - total_charge_cost
    print(profit, sell, buy, capacity, utilisation)

    residual_demand = [a - b for a, b in zip(demand, battery_dispatch)]

    avg_demand = [0] * 288
    avg_residual = [0] * 288
    
    avg_battery = [0] * 288
    avg_prices = [0] * 288
    avg_soc = [0] * 288

    for i in range(288):
        for j in range(365):
            avg_demand[i] += demand[j*288 + i] / 365
            avg_residual[i] += residual_demand[j*288 + i] / 365

            avg_battery[i] += (battery_dispatch[j*288 + i] / 365) / capacity
            avg_prices[i] += prices[j*288 + i] / 365
            avg_soc[i] += soc_list[j*288 + i] / 365

    ax1.plot(avg_demand)
    ax1.plot(avg_residual)
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(avg_prices)
    ax2.set_ylabel('Price ($/MWh)')

    ax3 = ax2.twinx()
    ax3.plot(avg_battery, color = 'green')
    ax3.plot(avg_soc, color = 'orange')

    ax2.set_title(folder.upper())
    ax2.set_xticks(range(0, 288, 36), range(0, 24, 3))
    ax2.set_xlim([0, 288])
    ax2.set_xlabel('Time of day')

    fig2.legend(['Spot price', 'Battery discharge', 'State of charge'], bbox_to_anchor=(1,1))
    fig2.tight_layout()
    fig2.savefig(f'figs/{folder} prices and battery')

ax1.set_ylabel('Demand (MW)')
ax1.set_xlabel('Time of day')
ax1.set_title("All states average demand")
ax1.set_xticks(range(0, 288, 36), range(0, 24, 3))
ax1.legend(['nsw', 'nsw', 'qld', 'qld', 'sa', 'sa', 'tas', 'tas', 'vic', 'vic'], bbox_to_anchor=(1,1))
ax1.set_xlim([0, 288])
fig1.tight_layout()
fig1.savefig(f'figs/all states demand')