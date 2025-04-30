from function_module.solar_functions import photovoltaics, solar_common, solar_scenario, solar_graphing
from function_module.solution_functions import solution_overview, warning_recommendation, solution_details


def solar_energy_pv_electricity_battery(latitude, longitude, resource_values, requirement_values): 
                         
    zenith_angle, azimuth_angle = solar_common.solar_position(latitude, longitude)
    optimum_zenith_angle, optimum_azimuth_angle, global_tilted_irradiance, global_tracker_irradiance = photovoltaics.radiation_calculation(
        latitude, resource_values["Global_Horizontal_Irradiance"], resource_values["Diffuse_Horizontal_Irradiance"], resource_values["Surface_Albedo"], zenith_angle, azimuth_angle)

    # The Average Scenario
    average_high_scenario = solar_scenario.photovoltaics_scenario(global_tracker_irradiance, resource_values["Air_Temperature"], requirement_values["Electricity"], "high", "Average")
    average_low_scenario = solar_scenario.photovoltaics_scenario(global_tilted_irradiance, resource_values["Air_Temperature"], requirement_values["Electricity"], "low", "Average")

    panel_position = solar_graphing.photovoltaics_panel_position(optimum_zenith_angle, optimum_azimuth_angle)
    average_scheme = solar_graphing.photovoltaics_electricity_battery_scheme("Average", average_low_scenario, average_high_scenario)

    #The Solution Overview
    final_solution_overview = solution_overview.solar_energy_pv_electricity_battery_overview(panel_position)

    photovoltaics_power = [average_high_scenario[0], average_low_scenario[0]]
    battery_capacity = [average_high_scenario[2], average_low_scenario[2]]
    hot_list = [average_high_scenario[7], average_low_scenario[7]]
    out_list = [average_high_scenario[8], average_low_scenario[8]]
    
    recommendation = warning_recommendation.solar_energy_pv_electricity_battery_recommendation(
        requirement_values["Electricity"], resource_values["Global_Horizontal_Irradiance"], photovoltaics_power, battery_capacity, hot_list, out_list)
    
    plot_list = [average_high_scenario[6], average_low_scenario[6]]
    zero_list = [average_high_scenario[9], average_low_scenario[9]]
        
    #The Solution Details
    final_solution_details = solution_details.solar_energy_pv_electricity_battery_details([average_scheme], recommendation, plot_list, hot_list, out_list, zero_list, latitude)
    
    return final_solution_overview, final_solution_details
