
def calculate_anomaly(hourly_raw_data, monthly_raw_data, leap_year, base_year, parameter, time_difference):
   
    import pandas as pd

    try:
        
        if parameter == "Diffuse_Horizontal_Irradiance":
            hourly_raw_data['DHI[unit="W m-2"]'] = hourly_raw_data['PARDF[unit="W m-2"]'] + hourly_raw_data['NIRDF[unit="W m-2"]']
            monthly_raw_data['DHI[unit="W m-2"]'] = monthly_raw_data['PARDF[unit="W m-2"]'] + monthly_raw_data['NIRDF[unit="W m-2"]']

        if parameter == "Surface_Albedo":
            hourly_raw_data.loc[hourly_raw_data['ALBEDO[unit="1"]'] > 1.0, 'ALBEDO[unit="1"]'] = 0.0

        column_name = {"Air_Temperature":'T2M[unit="K"]', 
                       "Global_Horizontal_Irradiance": 'SWGDN[unit="W m-2"]', 
                       "Surface_Albedo":'ALBEDO[unit="1"]', 
                       "Diffuse_Horizontal_Irradiance": 'DHI[unit="W m-2"]'}  #########

        if leap_year != True:
            hourly_data_frame = hourly_raw_data
        else:
            part1 = hourly_raw_data.loc[str(base_year) + "-01-01":str(base_year) + "-02-28"]
            part2 = hourly_raw_data.loc[str(base_year) + "-03-01":str(base_year) + "-12-31"]
            frames = [part1, part2]
            hourly_data_frame = pd.concat(frames)

        zero_mask = []
        for i in hourly_data_frame[column_name[parameter]]:
            try:
                zero_mask.append(i/i)
            except ZeroDivisionError:
                zero_mask.append(0.0)

        resampled_hourly_data = hourly_data_frame.resample('ME').mean()
        grouped_monthly_data = monthly_raw_data.groupby(monthly_raw_data.index.month).mean()
    
        difference = list()
        for i in range(len(list(grouped_monthly_data[column_name[parameter]]))):
            anomaly = list(resampled_hourly_data[column_name[parameter]])[i] - list(grouped_monthly_data[column_name[parameter]])[i]
            difference.append(anomaly)
    
        part_1 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-01-01":str(base_year) + "-01-31"] - difference[0]
        part_2 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-02-01":str(base_year) + "-02-28"] - difference[1]
        part_3 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-03-01":str(base_year) + "-03-31"] - difference[2]
        part_4 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-04-01":str(base_year) + "-04-30"] - difference[3]
        part_5 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-05-01":str(base_year) + "-05-31"] - difference[4]
        part_6 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-06-01":str(base_year) + "-06-30"] - difference[5]
        part_7 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-07-01":str(base_year) + "-07-31"] - difference[6]
        part_8 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-08-01":str(base_year) + "-08-31"] - difference[7]
        part_9 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-09-01":str(base_year) + "-09-30"] - difference[8]
        part_10 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-10-01":str(base_year) + "-10-31"] - difference[9]
        part_11 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-11-01":str(base_year) + "-11-30"] - difference[10]
        part_12 = hourly_raw_data[column_name[parameter]].loc[str(base_year) + "-12-01":str(base_year) + "-12-31"] - difference[11]
        frames1 = [part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8, part_9, part_10, part_11, part_12]
        time_series_data = pd.concat(frames1)
    
        final_data= []
        for i in time_series_data:
        
            if (parameter == "Global_Horizontal_Irradiance" or parameter == "Diffuse_Horizontal_Irradiance"):
                if i < 0:
                    final_data.append(0.0)
                else:
                    final_data.append(i)
                
            elif parameter == "Surface_Albedo":
                if (i < 0 or i > 1):
                    final_data.append(0.0)
                else:
                    final_data.append(i)

            else:
                final_data.append(i)
    
        final_list = []
        for i in range(0,len(final_data)):
            final_list.append(final_data[i] * zero_mask[i])

        final_list =  final_list[time_difference:] + final_list[:time_difference]

    except Exception as e:
        final_list = None
    
    return final_list


def annual_hourly_average(data):
    
    import pandas as pd 

    date_time_index = pd.date_range(start="2025-01-01T00:00:00",end="2025-12-31T23:00:00", freq="1h")
    date_frame = pd.DataFrame(data,date_time_index)
    hourly_average = date_frame.groupby(date_frame.index.hour).mean()
    average_hourly = hourly_average.values.tolist()
    annual_hourly_average = []
    for i in average_hourly:
        annual_hourly_average.append(i[0]) 

    return annual_hourly_average
