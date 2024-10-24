import pandas as pd
import pvlib
import numpy as np
import matplotlib.pyplot as plt

def calculatesolar():
    """Function that returns the average solar output in Perth Australia"""

    #Average temperature in Perth Australia, for source see sources.txt
    average_temperature = [23.9, 23.9, 22.2, 18.9, 16.1, 13.9, 12.8, 13.3, 14.4, 16.7, 19.4, 21.7]

    #Average solar irradiance in Perth Australia in MJ/day/m^2, for source see sources.txt
    average_irradiance_megajoule = np.array([29.2, 25.9, 21.0, 15.2, 11.2, 9.3,
                                    9.9, 13.0, 17.0, 22.6, 26.8, 30.0])
    #Calculate it to W/m^2
    average_irradiance_watt = average_irradiance_megajoule*1000000/(24*60*60)

    # Create a time index for 1 year with monthly intervals
    time_index = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')

    # Create a list of values representing monthly solar irradiance data
    solar_irradiance = pd.Series(average_irradiance_watt, index=time_index)

    # Simulate varying cell temperatures for each month (example data)
    temp_cell = pd.Series(average_temperature, index=time_index)  # Start at 20°C

    # Create a PV system with proper module parameters
    # You can adjust these values according to specific PV module data
    module_parameters = {
        'pdc0': 250,          # Nominal power at STC in W
        'gamma_pdc': -0.004,  # Temperature coefficient (%/°C)
        'alpha': 0.000,       # Module temperature coefficient (K^-1)
        'beta': 0.0,          # Voltage temperature coefficient (V/K)
    }

    # Step 1: Define the PV system
    solar_panel = pvlib.pvsystem.PVSystem(
        surface_tilt=30,
        surface_azimuth=180,
        module_parameters=module_parameters,
    )

    # Calculate the solar output in kW using pvwatts_dc
    solar_output_watt = solar_panel.pvwatts_dc(solar_irradiance, temp_cell)

    # Converting the watts to kilowatts
    solar_output_kilowatt = np.array(solar_output_watt)/1000

    #Averaging the days in the month to 30 for simplicity. 
    solar_output_kwh = solar_output_kilowatt * 30 * 24

    # Create a Pandas Series to store the result and format it like the example
    solar_output_series = pd.Series(solar_output_kwh, index=time_index)

    return solar_output_series
    # # Calculate the solar output using pvwatts_dc()
    # solar_pannel_output = solar_panel.pvwatts_dc(solar_irradiance, temp_cell)

    # return solar_pannel_output

solar_output = calculatesolar()

# Display the solar output for each month
print(solar_output)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(solar_output, label="Solar Output (Kilowatthour/month)")
# plt.plot(time_index, wind_output, label="Wind Output (kW)")
# plt.plot(time_index, house_consumption, label="House Consumption (kW)")
# plt.plot(time_index, net_power_flow_series, label="Net Power Flow (kW)")
# plt.plot(time_index, battery_state_of_charge_series, label="Battery SOC (kWh)")
plt.xlabel("Time")
plt.ylabel("Power (kWh)")
plt.title("Smart DC House Simulation with Custom Battery Model")
plt.legend()
plt.grid(True)
plt.show()