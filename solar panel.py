import pandas as pd
import pvlib
import numpy as np

#Average temperature in Perth Australia
average_temperature = [23.9, 23.9, 22.2, 18.9, 16.1, 13.9, 12.8, 13.3, 14.4, 16.7, 19.4, 21.7]

#Average solar irradiance in Perth Australia in MJ/day/m^2
average_irradiance_MJ = np.array([29.2, 25.9, 21.0, 15.2, 11.2, 9.3,
                                   9.9, 13.0, 17.0, 22.6, 26.8, 30.0])
#Calculate it to W/m^2
average_irradiance_W = average_irradiance_MJ*1000000/(24*60*60)

# Create a time index for 1 year with monthly intervals
time_index = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')

# Create a list of values representing monthly solar irradiance data
solar_irradiance = pd.Series(average_irradiance_W, index=time_index)

# Simulate varying cell temperatures for each month (example data)
temp_cell = pd.Series(average_temperature, index=time_index)  # Start at 20°C

# Create a PV system with proper module parameters
# You can adjust these values according to specific PV module data
module_parameters = {
    'pdc0': 4000,          # Nominal power at STC in W
    'gamma_pdc': -0.004,  # Temperature coefficient (%/°C)
    'alpha': 0.003,       # Module temperature coefficient (K^-1)
    'beta': 0.0,          # Voltage temperature coefficient (V/K)
}

# Step 1: Define the PV system
solar_panel = pvlib.pvsystem.PVSystem(
    surface_tilt=30,
    surface_azimuth=180,
    module_parameters=module_parameters,
)

# Calculate the solar output using pvwatts_dc()
solar_output = solar_panel.pvwatts_dc(solar_irradiance, temp_cell)

# Display the solar output for each month
print(solar_output)
