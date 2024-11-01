"""Simulation code for systems engineering"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from solar_panel import calculatesolar
from wind_turbine import calculatewind
from tidal_power import calculatetidal

apartments = 60
solar_panels = 100
tidal_power_plants = 0
wind_turbines = 2

solar_output = solar_panels * calculatesolar()
wind_output = wind_turbines * calculatewind()
tidal_output = tidal_power_plants * calculatetidal()

household_load = np.array([340, 350, 405, 430, 495, 630,
                            510, 460, 450, 460, 402, 498]) * apartments * 1.25 #times 1.25 for the fact that every house has a EV.

# Create a time index for 1 year with monthly intervals
time_index = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')

household_load = pd.Series(data = household_load, index = time_index)

total_power_output = np.array(solar_output) + np.array(tidal_output) + np.array(wind_output)

total_power_output = pd.Series(data = total_power_output, index = time_index)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(solar_output, label="Solar output")
plt.plot(wind_output, label="Wind output")
#plt.plot(tidal_output, label="Tidal output")
plt.plot(household_load, label = "Household load")
plt.plot(total_power_output, label = "Total power output")

plt.xlabel("Time")
plt.ylabel("Energy (kWh)")
plt.xlim([solar_output.index.min(), solar_output.index.max()])
plt.title("Smart DC House Simulation")
plt.legend()
plt.grid(True)
plt.savefig("energy-outputs.svg", format="svg")
plt.show()
