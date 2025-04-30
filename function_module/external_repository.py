
def create_link(latitude, longitude, parameter):
    
    import pytz, calendar
    from datetime import datetime,timezone
    from timezonefinder import TimezoneFinder
    
    timezone_object = TimezoneFinder()
    selected_timezone = timezone_object.timezone_at(lng=longitude, lat=latitude)
    final_timezone = pytz.timezone(selected_timezone)
    selected_current_time = datetime.now(final_timezone)
    utc_current_time = datetime.now(timezone.utc)
    time_difference = round((utc_current_time.hour + utc_current_time.minute / 60) - (selected_current_time.hour + selected_current_time.minute / 60))
    
    if utc_current_time.month > 1:
        base_year = utc_current_time.year - 1
    else:
        base_year = utc_current_time.year - 2 
    base_year_anomaly = base_year - 29
    leap_year = calendar.isleap(base_year)

    if parameter == "Air_Temperature":
        hourly_url = ["https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_aggregation/M2T1NXSLV.5.12.4/M2T1NXSLV.5.12.4_Aggregation_" + str(base_year) + ".ncml?var=T2M&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T23%3A30%3A00Z&accept=csv_file"] 
        monthly_url = ["https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_MONTHLY_aggregation/M2TMNXSLV.5.12.4_Aggregation.ncml?var=T2M&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year_anomaly) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T00%3A30%3A00Z&accept=csv_file"]
    
    elif (parameter == "Global_Horizontal_Irradiance" or parameter == "Surface_Albedo"):   
        hourly_url = ["https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_aggregation/M2T1NXRAD.5.12.4/M2T1NXRAD.5.12.4_Aggregation_" + str(base_year) + ".ncml?var=ALBEDO&var=SWGDN&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T23%3A30%3A00Z&accept=csv_file"]
        monthly_url = ["https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_MONTHLY_aggregation/M2TMNXRAD.5.12.4_Aggregation.ncml?var=ALBEDO&var=SWGDN&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year_anomaly) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T00%3A30%3A00Z&accept=csv_file"]

    elif parameter == "Diffuse_Horizontal_Irradiance":
        hourly_url = ["https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_aggregation/M2T1NXLFO.5.12.4/M2T1NXLFO.5.12.4_Aggregation_" + str(base_year) + ".ncml?var=PARDF&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T23%3A30%3A00Z&accept=csv_file",
                     "https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_aggregation/M2T1NXFLX.5.12.4/M2T1NXFLX.5.12.4_Aggregation_" + str(base_year) + ".ncml?var=NIRDF&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T23%3A30%3A00Z&accept=csv_file"
                    ]
        monthly_url = ["https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_MONTHLY_aggregation/M2TMNXLFO.5.12.4_Aggregation.ncml?var=PARDF&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year_anomaly) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T00%3A30%3A00Z&accept=csv_file",
                      "https://goldsmr4.gesdisc.eosdis.nasa.gov/thredds/ncss/MERRA2_MONTHLY_aggregation/M2TMNXFLX.5.12.4_Aggregation.ncml?var=NIRDF&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&time_start=" + str(base_year_anomaly) + "-01-01T00%3A30%3A00Z&time_end=" + str(base_year) + "-12-31T00%3A30%3A00Z&accept=csv_file"
                    ]
                      
    return hourly_url, monthly_url, leap_year, base_year, time_difference


def send_request(hourly_url, monthly_url, username, password):
    
    import io
    import pandas as pd
    from urllib import request
    from http import cookiejar

    top_level_url = "https://urs.earthdata.nasa.gov"

    created_request = request.HTTPPasswordMgrWithDefaultRealm()
    created_request.add_password(None, top_level_url, username, password)

    authorization_handler = request.HTTPBasicAuthHandler(created_request)
    authorization_cookie_jar = cookiejar.CookieJar()
    cookie_jar = request.HTTPCookieProcessor(authorization_cookie_jar)
    opener = request.build_opener(authorization_handler, cookie_jar)

    request.install_opener(opener)

    column_name = ['T2M[unit="K"]',  
                   'SWGDN[unit="W m-2"]', 
                   'ALBEDO[unit="1"]', 
                   'PARDF[unit="W m-2"]', 
                   'NIRDF[unit="W m-2"]'] ##############
    
    hourly_raw_data = pd.DataFrame({"A" : []})
    for i in hourly_url:
        try:
            request_hourly_data = request.Request(i)
            response_hourly_data = request.urlopen(request_hourly_data)

            hourly_raw_file = response_hourly_data.read()
            hourly_raw_bite = io.BytesIO(hourly_raw_file)

            hourly_data_frame = pd.read_csv(hourly_raw_bite, sep=",", header=0, index_col=0, parse_dates=True)
            hourly_column_name = hourly_data_frame.columns.tolist()
            
            for j in hourly_column_name:
                for k in column_name:
                    if j==k:
                        hourly_raw_data[j] = hourly_data_frame[j]
                    else:
                        continue
        
        except Exception as e:
            hourly_raw_data = pd.DataFrame({"A" : []})
    
    monthly_raw_data = pd.DataFrame({"A" : []})
    for i in monthly_url:
        try:
            request_monthly_data = request.Request(i)
            response_monthly_data = request.urlopen(request_monthly_data)

            monthly_raw_file = response_monthly_data.read()
            monthly_raw_bite = io.BytesIO(monthly_raw_file)

            monthly_data_frame = pd.read_csv(monthly_raw_bite, sep=",", header=0, index_col=0, parse_dates=True)
            monthly_column_name = monthly_data_frame.columns.tolist()
            
            for j in monthly_column_name:
                for k in column_name:
                    if j==k:
                        monthly_raw_data[j] = monthly_data_frame[j]
                    else:
                        continue
        
        except Exception as e:
            monthly_raw_data = pd.DataFrame({"A" : []})

    return hourly_raw_data, monthly_raw_data