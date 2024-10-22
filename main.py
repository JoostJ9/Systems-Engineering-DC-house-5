"""Simulation code for systems engineering"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from solar_panel import calculatesolar
from wind_turbine import calculatewind
from tidal_power import calculatetidal

# Define the custom battery class from above (SimpleBattery)
class Battery:
    """Class to replicate the behaviour of a battery"""
    def __init__(self, capacity_kwh, efficiency=0.95):
        self.capacity_kwh = capacity_kwh  # Total battery capacity in kWh
        self.efficiency = efficiency  # Charging/discharging efficiency
        self.soc = 0  # Start fully charged by default

    def charge(self, power_kwh):
        """Charging the battery"""
        charge_energy = power_kwh * self.efficiency  # Effective energy stored
        self.soc += charge_energy
        if self.soc > self.capacity_kwh:
            charge_energy = self.capacity_kwh - (self.soc - charge_energy)
            self.soc = self.capacity_kwh  # Cap SOC at max capacity
        return charge_energy / self.efficiency  # Return energy used for charging

    def discharge(self, power_kwh):
        """Discharging the battery"""
        discharge_energy = power_kwh
        if discharge_energy > self.soc:
            discharge_energy = self.soc  # Limit discharge to available energy
        self.soc -= discharge_energy
        return discharge_energy  # Return energy supplied

    def get_soc(self):
        """Get the amount of energy stored in the battery"""
        return self.soc

# Battery Setup (using the custom SimpleBattery class)
battery = Battery(capacity_kwh=10, efficiency=0.95)
battery_state_of_charge = []  # Keep track of the state of charge

solar_output = 60*8*calculatesolar()
wind_output = calculatewind()
tidal_output = 5*calculatetidal()

# Initialize variables
net_power_flow = []
battery_soc = battery.capacity_kwh

# # Smart House Simulation: Track net power flow and battery usage
# for hour in time_index:
#     solar_power = solar_output.loc[hour]  # Power from solar panel (kW)
#     wind_power = wind_output.loc[hour]    # Power from wind turbine (kW)
#     house_power = house_consumption.loc[hour]  # Power demand of the house (kW)

#     # Total generation (DC from solar and wind)
#     total_generation = solar_power + wind_power

#     # Net power flow to the house (generation - consumption)
#     net_flow = total_generation - house_power

#     # Handle battery charge/discharge
#     if net_flow > 0:
#         # Surplus power, charge battery
#         charge_power = min(net_flow, battery.max_charge_kW)
#         energy_used_for_charging = battery.charge(charge_power, 1)  # Assume 1-hour interval
#         net_flow -= energy_used_for_charging  # Adjust net flow after charging
#     else:
#         # Deficit power, discharge battery
#         discharge_power = min(-net_flow, battery.max_discharge_kW)
#         energy_supplied_by_battery = battery.discharge(discharge_power, 1)  # Assume 1-hour interval
#         net_flow += energy_supplied_by_battery  # Adjust net flow after discharge

#     # Record results
#     battery_state_of_charge.append(battery.get_soc())
#     net_power_flow.append(net_flow)

# # Convert results to a pandas series for easy plotting
# net_power_flow_series = pd.Series(net_power_flow, index=time_index)
# battery_state_of_charge_series = pd.Series(battery_state_of_charge, index=time_index)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(solar_output, label="Solar Output (kW)")
plt.plot(wind_output, label="Wind Output (kW)")
plt.plot(tidal_output, label="Tidal Output (kW)")
# plt.plot(house_consumption, label="House Consumption (kW)")
# plt.plot(time_index, net_power_flow_series, label="Net Power Flow (kW)")
# plt.plot(time_index, battery_state_of_charge_series, label="Battery SOC (kWh)")
plt.xlabel("Time")
plt.ylabel("Power (kW) / Battery SOC (kWh)")
plt.title("Smart DC House Simulation with Custom Battery Model")
plt.legend()
plt.grid(True)
plt.show()
