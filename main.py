"""Simulation code for systems engineering"""

import pvlib
from windpowerlib import ModelChain, WindTurbine
import pandas as pd
import matplotlib.pyplot as plt

# Define the custom battery class from above (SimpleBattery)
class SimpleBattery:
    """Class to replicate the behaviour of a battery"""
    def __init__(self, capacity_kWh, max_discharge_kW, max_charge_kW, efficiency=0.95):
        self.capacity_kWh = capacity_kWh  # Total battery capacity in kWh
        self.max_discharge_kW = max_discharge_kW  # Max power the battery can discharge in kW
        self.max_charge_kW = max_charge_kW  # Max power the battery can charge in kW
        self.efficiency = efficiency  # Charging/discharging efficiency
        self.soc = capacity_kWh  # Start fully charged by default

    def charge(self, power_kW, duration_h):
        charge_energy = power_kW * duration_h * self.efficiency  # Effective energy stored
        self.soc += charge_energy
        if self.soc > self.capacity_kWh:
            charge_energy = self.capacity_kWh - (self.soc - charge_energy)
            self.soc = self.capacity_kWh  # Cap SOC at max capacity
        return charge_energy / self.efficiency  # Return energy used for charging

    def discharge(self, power_kW, duration_h):
        discharge_energy = power_kW * duration_h
        if discharge_energy > self.soc:
            discharge_energy = self.soc  # Limit discharge to available energy
        self.soc -= discharge_energy
        return discharge_energy  # Return energy supplied

    def get_soc(self):
        return self.soc


# Set up time series for simulation, 1 per month for a whole year
time_index = pd.date_range(start='2024-01-01', end='2025-12-01', freq='MS')

# Solar PV Setup
location = pvlib.location.Location(latitude=35, longitude=-120, tz='Etc/GMT+8')
solar_irradiance = pd.Series([400 + i * 50 for i in range(len(time_index))], index=time_index)

# Step 3: Simulate cell temperatures (for simplicity, using a constant value)
# In practice, you would model temperature variations
temp_cell = 25  # Average cell temperature in degrees Celsius

solar_panel = pvlib.pvsystem.PVSystem(surface_tilt=30, surface_azimuth=180, module_parameters={'pdc0': 4000, 'gamma_pdc': 0,  'beta': 0.0, })  # 4kW panel
solar_output = solar_panel.pvwatts_dc(solar_irradiance, temp_cell)

# Wind Turbine Setup
wind_turbine_specs = {
    'turbine_type': 'Vestas_V80_2000',  # Sample 2 MW turbine
    'hub_height': 80
}
wind_turbine = WindTurbine(**wind_turbine_specs)
wind_speed_series = pd.Series([5 + 0.1 * i for i in range(24)], index=time_index)  # Simplified wind speed data

# Create a model chain to simulate wind turbine output
model_chain = ModelChain(wind_turbine)
wind_output = model_chain.run_model(weather={'wind_speed': wind_speed_series}).power_output / 1000  # in kW

# Battery Setup (using the custom SimpleBattery class)
battery = SimpleBattery(capacity_kWh=10, max_discharge_kW=5, max_charge_kW=5, efficiency=0.95)
battery_state_of_charge = []  # Keep track of the state of charge

# House Consumption (random daily profile in kW)
house_consumption = pd.Series([2 + 0.5 * (i % 4) for i in range(24)], index=time_index)

# Initialize variables
net_power_flow = []
battery_soc = battery.capacity_kWh

# Smart House Simulation: Track net power flow and battery usage
for hour in time_index:
    solar_power = solar_output.loc[hour]  # Power from solar panel (kW)
    wind_power = wind_output.loc[hour]    # Power from wind turbine (kW)
    house_power = house_consumption.loc[hour]  # Power demand of the house (kW)

    # Total generation (DC from solar and wind)
    total_generation = solar_power + wind_power

    # Net power flow to the house (generation - consumption)
    net_flow = total_generation - house_power

    # Handle battery charge/discharge
    if net_flow > 0:
        # Surplus power, charge battery
        charge_power = min(net_flow, battery.max_charge_kW)
        energy_used_for_charging = battery.charge(charge_power, 1)  # Assume 1-hour interval
        net_flow -= energy_used_for_charging  # Adjust net flow after charging
    else:
        # Deficit power, discharge battery
        discharge_power = min(-net_flow, battery.max_discharge_kW)
        energy_supplied_by_battery = battery.discharge(discharge_power, 1)  # Assume 1-hour interval
        net_flow += energy_supplied_by_battery  # Adjust net flow after discharge

    # Record results
    battery_state_of_charge.append(battery.get_soc())
    net_power_flow.append(net_flow)

# Convert results to a pandas series for easy plotting
net_power_flow_series = pd.Series(net_power_flow, index=time_index)
battery_state_of_charge_series = pd.Series(battery_state_of_charge, index=time_index)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(time_index, solar_output, label="Solar Output (kW)")
plt.plot(time_index, wind_output, label="Wind Output (kW)")
plt.plot(time_index, house_consumption, label="House Consumption (kW)")
plt.plot(time_index, net_power_flow_series, label="Net Power Flow (kW)")
plt.plot(time_index, battery_state_of_charge_series, label="Battery SOC (kWh)")
plt.xlabel("Time")
plt.ylabel("Power (kW) / Battery SOC (kWh)")
plt.title("Smart DC House Simulation with Custom Battery Model")
plt.legend()
plt.grid(True)
plt.show()
