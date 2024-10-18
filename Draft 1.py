#SIMULATION PLAN

# Household energy usage for each month in kWh
household_load = [300, 320, 280, 290, 350, 360, 340, 330, 310, 300, 290, 310]

cost_per_solar_panel = 200  # Cost per solar panel
cost_per_wind_turbine = 1000  # Cost per wind turbine
cost_per_tidal_plant = 5000  # Cost per tidal plant 

energy_per_solar_panel = 30  # kWh per solar panel per month
energy_per_wind_turbine = 120  # kWh per wind turbine per month
energy_per_tidal_plant = 300  # kWh per tidal plant per month 

def get_user_input():
    """
    Function to get user input for energy generated by solar, wind, and tidal sources, and the selected month.
    """
    solar_energy = float(input("Enter the solar energy generated per month (kWh): "))
    wind_energy = float(input("Enter the wind energy generated per month (kWh): "))
    tidal_energy = float(input("Enter the tidal energy generated per month (kWh): "))
    month = int(input("Enter the month of interest (1 for January, 2 for February, etc.): ")) - 1
    return solar_energy, wind_energy, tidal_energy, month

def calculate_combined_energy(solar, wind, tidal, month):
    """
    Calculate the energy generated by different combinations: Solar + Wind, Solar + Tidal, Wind + Tidal.
    """
    # Load requirement for the selected month
    load_required = household_load[month]
    
    # Possible combinations of energy sources
    combinations = {
        "Solar + Wind": solar + wind,
        "Solar + Tidal": solar + tidal,
        "Wind + Tidal": wind + tidal
    }

    return combinations, load_required

def calculate_cost(solar_energy, wind_energy, tidal_energy):
    """
    Calculate the cost of the setup based on the energy generated by solar, wind, and tidal.
    """
    # Calculate the number of units needed to meet the energy generated
    num_solar_panels = round(solar_energy / energy_per_solar_panel)
    num_wind_turbines = round(wind_energy / energy_per_wind_turbine)
    num_tidal_plants = 1 

    # Total cost calculation
    total_cost = (num_solar_panels * cost_per_solar_panel) + (num_wind_turbines * cost_per_wind_turbine) + (num_tidal_plants * cost_per_tidal_plant)
    return total_cost, num_solar_panels, num_wind_turbines, num_tidal_plants

def main():
    # Get user inputs
    solar_energy, wind_energy, tidal_energy, month = get_user_input()
    
    # Calculate combined energy and the load requirement for the selected month
    combinations, load_required = calculate_combined_energy(solar_energy, wind_energy, tidal_energy, month)
    
    best_combination = None
    min_cost = float('inf')  # Set to infinity initially
    best_config = {}

    print(f"Load required for month {month + 1}: {load_required} kWh\n")
    
    # Check each combination and calculate cost
    for combo_name, total_energy in combinations.items():
        print(f"Combination: {combo_name}")
        print(f"Total Energy Generated: {total_energy} kWh")

        if total_energy >= load_required:
            print(f"Energy requirement met for {combo_name}.")

            # Calculate the cost of this combination
            solar_in_combo = solar_energy if "Solar" in combo_name else 0
            wind_in_combo = wind_energy if "Wind" in combo_name else 0
            tidal_in_combo = tidal_energy if "Tidal" in combo_name else 0

            cost, num_solar_panels, num_wind_turbines, num_tidal_plants = calculate_cost(solar_in_combo, wind_in_combo, tidal_in_combo)
            print(f"Total Cost: ${cost:.2f}")
            print(f"Solar Panels: {num_solar_panels:.2f}, Wind Turbines: {num_wind_turbines:.2f}, Tidal Plants: {num_tidal_plants}\n")

            # Check if this is the cheapest combination
            if cost < min_cost:
                min_cost = cost
                best_combination = combo_name
                best_config = {
                    "Cost": cost,
                    "Solar Panels": num_solar_panels,
                    "Wind Turbines": num_wind_turbines,
                    "Tidal Plants": num_tidal_plants
                }

        else:
            # Calculate the energy deficit
            deficit = load_required - total_energy
            print(f"Energy requirement NOT met. Deficit: {deficit:.2f} kWh\n")

    # Output the best combination and its cost
    if best_combination:
        print(f"The cheapest combination is {best_combination} with a total cost of ${min_cost:.2f}.")
        print(f"Configuration: {best_config}")
    else:
        print("No combination met the energy requirement.")

# Run the main function
main()