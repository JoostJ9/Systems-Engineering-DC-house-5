import pandas as pd
from windpowerlib import WindTurbine, ModelChain
from windpowerlib import data as wt
from matplotlib import pyplot as plt
import numpy as np

def calculatewind():
    """Function that returns the average wind turbine output using windpowerlib"""
    
    # Define the wind turbine based on a standard turbine model in the library
    turbine_data = {
        'turbine_type': 'E-126/4200',  # Example turbine (Enercon E-126, 4.2MW rated power)
        'hub_height': 135  # Hub height in meters
    }
    
    # Instantiate a WindTurbine object
    turbine = WindTurbine(**turbine_data)
    
    # Average wind speed in Perth (miles/hour) (example data)
    average_wind_speed_miles_hour = np.array([14.0, 13.7, 12.9, 11.8, 11.8, 12.6,
                          12.5, 12.1, 12.2, 12.5, 13.4, 13.9])
    
    #Convert it to m/s
    average_wind_speed_ms = average_wind_speed_miles_hour*0.44704
    
    # Assuming constant average temperature (in Celsius)
    temperature = [23.9, 23.9, 22.2, 18.9, 16.1, 13.9, 12.8, 13.3, 14.4, 16.7, 19.4, 21.7]

    # Roughness length in meters (example for flat rural areas)
    roughness_length = [0.1] * 12  # Constant roughness length for each month

    # Create a time index for 1 year with monthly intervals
    time_index = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')

    # Create a DataFrame for wind speed, temperature, and roughness length over time with a multi-level index
    weather_df = pd.DataFrame({
        ('wind_speed', 10): average_wind_speed_ms,    # Wind speed at 10m height
        ('temperature', 2): temperature,           # Temperature at 2m height
        ('roughness_length', ''): roughness_length # Roughness length (dimensionless)
    }, index=time_index)

    # Create a ModelChain object to calculate the power output
    modelchain = ModelChain(turbine)
    
    # Run the model chain for power output calculation
    modelchain.run_model(weather_df)

    # Extract the power output in kW
    power_output_kw = modelchain.power_output
    
    # Assume each month has 30 days to calculate the energy in kWh
    energy_output_kwh = power_output_kw * 30 * 24  # kWh per month
    
    return energy_output_kwh


# Calculate wind turbine output using windpowerlib
wind_output = calculatewind()

# Display the wind turbine output for each month
print(wind_output)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(wind_output, label="Wind Output (Kilowatthour/month)")
plt.xlabel("Time")
plt.ylabel("Power (kWh)")
plt.title("Wind Turbine Output Simulation")
plt.legend()
plt.grid(True)
plt.show()

df = wt.get_turbine_types(print_out=True)

# find all Enercons
print(df[df["manufacturer"].str.contains("Enercon")])
