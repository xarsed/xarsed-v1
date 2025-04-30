
def series_parameter(value):

    # Resource parameters

    if value == "solarEnergyPV":
        series_parameter = ["Air_Temperature",
                          "Global_Horizontal_Irradiance",
                          "Diffuse_Horizontal_Irradiance",
                          "Surface_Albedo"] 

    # Requirement parameters

    elif value == "electricity":
        series_parameter = ["Electricity"] #####

    else:
        series_parameter = []
    
    return series_parameter


def create_list(file, parameter):
    
    import io, csv

    decoded_file = file.read().decode()
    io_string = io.StringIO(decoded_file)
    csv_file = csv.reader(io_string, quoting=csv.QUOTE_NONNUMERIC)
    
    try:

        final_list = []
        for row in csv_file:
            for data in row:
                
                if (parameter == "Global_Horizontal_Irradiance" or parameter == "Diffuse_Horizontal_Irradiance" or parameter == "Electricity"):
                    
                    if data < 0:
                        final_list.append(0)
                    else:
                        final_list.append(data)
                
                elif parameter == "Surface_Albedo":
                    
                    if (data < 0 or data > 1):
                        final_list.append(0)
                    else:
                        final_list.append(data)

                else:
                    final_list.append(data)
        
        if sum(final_list) == 0:
            
            final_list = None
    
    except ValueError:
        
        final_list = None
    
    return final_list


def appliance_list(parameter):
    
    if parameter == 'Electricity':
        
        noun = '<option>None</option>'
        group1 = '<optgroup label="Always on"><option>WiFi router</option><option>home security system</option></optgroup>'
        group2 = '<optgroup label="Continuous operation with automatic shutdown"><option>refrigerator</option><option>freezer</option></optgroup>'
        group3 = '<optgroup label="Daily usage"><option>electric stove</option><option>electric water heater</option></optgroup>'
        group4 = '<optgroup label="Weekly usage"><option>washing machine</option><option>dryer</option></optgroup>'
        group5 = '<optgroup label="Seasonal usage"><option>air conditioner</option><option>heater</option></optgroup>'
        appliance_list = noun + group1 + group2 + group3 + group4 + group5
        consumption_unit = "Watt"
    
    else:
        
        appliance_list = ""
        consumption_unit = ""
    
    return appliance_list, consumption_unit


def generate_table_list(parameter, appliance, appliance_name, appliance_consumption, appliance_count, appliance_efficiency, seasons, months, weeks, days, specfic_day, hours, appliance_usage, consumption_table, consumption_list):
    
    if seasons == []:
        season_index = list(range(1, 5))
    else:
        season_index = [int(item) for item in seasons]

    if months == []:
        month_index = list(range(1, 13))
    else:
        month_index = [int(item) for item in months]

    if weeks == []:
        week_index = list(range(1, 49))
    else:
        weeks_index = [int(item) for item in weeks]
        week_index = []
        for i in month_index:
            for j in weeks_index:
                week_index.append(4 * (i - 1) + j)

    if days == []:
        day_index = list(range(1, 8))
    else:
        day_index = [int(item) for item in weeks]
    
    all_day_index = list(range(1, 366))

    selected_day_index = []
    for i in season_index: 
        for j in month_index: 
            for k in week_index:
                if (3*i-2 <= j and j <= 3*i):
                    if (4*j-3 <= k and k <= 4*j):
                        first_index = 7 * (k - 1) + (2 * j - 1) + i + 1
                        last_index = 7 * k + (2 * j - 1) + i + 1
                        final_index = all_day_index[first_index:last_index]
                        for l in day_index:
                            selected_day_index.append(final_index[l-1])

    if specfic_day != "":
        specfic_day_index = [int(specfic_day)]
    else:
        specfic_day_index = []

    if specfic_day_index == []:
        final_day_index = selected_day_index
    else:
        if (seasons == [] and months == [] and weeks == [] and days == []):
            final_day_index = specfic_day_index
        else:
            if specfic_day_index[0] in selected_day_index:
                final_day_index = selected_day_index
            else:
                final_day_index = selected_day_index + specfic_day_index
                final_day_index.sort()

    if hours == []:
        hour_index = list(range(0, 24))
    else:
        hour_index = [int(item) for item in hours]

    all_index = []
    for i in final_day_index:
        for j in hour_index:
            all_index.append(24 * (i - 1) + j)

    #Correction Factor for Dropped Day Index
    correction_factor = 365.0 / (365.0 - 29.0)
    
    consumption_hourly_average = appliance_consumption * appliance_count * appliance_usage * correction_factor * 100.0 / (60.0 * appliance_efficiency) #[consumptions]
    
    for i in all_index:
        consumption_list[i] += consumption_hourly_average

    appliance_annual_consumption = len(all_index) * consumption_hourly_average
    consumption_daily_average = appliance_annual_consumption * 3600.0 / 365.0 #[consumptions/day] 
    consumption_monthly_total = sum(consumption_list) * 3600.0 / 12.0 #[total consumptions/month]
    
    if parameter == "Electricity":
        average_daily_consumption = consumption_daily_average / 3600000.0 # for Electricity [J/day] convert to [kW.h/day]
        total_monthly_consumption = consumption_monthly_total / 3600000.0 # [kW.h/month]
        parameter_unit = "kW.h"

    else:
        average_daily_consumption = 0.0
        total_monthly_consumption = 0.0
        parameter_unit = ""

    given_name = bool(appliance_name and not appliance_name.isspace())
    if given_name == True:
        if appliance != "None":
            name = appliance_name
        else:
            name = appliance_name
    else:
        if appliance != "None":
            name = appliance
        else:
            name = "appliance"

    new_row = '<tr><td>'+name+'</td><td>'+str(appliance_consumption)+'</td><td>'+str(appliance_count)+'</td><td>'+str(round(average_daily_consumption, 2))+'</td></tr>'
    
    if consumption_table == "":
        header = '<thead><tr><th>Name</th><th>Consumption</th><th>Number</th><th>Average Daily Consumption ['+parameter_unit+']</th></tr></thead>'
        footer = '<tfoot><tr><td>Total Average Monthly Consumption</td><td colspan="3">'+str(round(total_monthly_consumption, 2))+'['+parameter_unit+']</td></tr></tfoot>'
        new_consumption_table = header + new_row + footer

    else:
        footer_index = consumption_table.find("<tfoot>")
        footer = '<tfoot><tr><td>Total Average Monthly Consumption</td><td colspan="3">'+str(round(total_monthly_consumption, 2))+'['+parameter_unit+']</td></tr></tfoot>'
        new_consumption_table = consumption_table[:footer_index] + new_row + footer

    return new_consumption_table, consumption_list 
