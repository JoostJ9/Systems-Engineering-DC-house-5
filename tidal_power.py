import pandas as pd
import matplotlib.pyplot as plt

def calculatetidal():
    """Calculate the average tidal power per month"""
    # Create a time index for 1 year with monthly intervals
    time_index = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    tidal_power_kwh = [1000*24*30] *12 #taken 1MW for simplicity. 
    tidal_power = pd.Series(tidal_power_kwh, time_index)
    return tidal_power

# Calculate tidal output
tidal_output =  calculatetidal()

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(tidal_output, label="Tidal output (Kilowatthour/month)")
plt.xlabel("Time")
plt.ylabel("Power (kWh)")
plt.title("Tidal power plant output Simulation")
plt.legend()
plt.grid(True)
plt.show()
