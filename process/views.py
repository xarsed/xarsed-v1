from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from xarsed.common.common import series_parameter, create_list, appliance_list, generate_table_list
from xarsed.solution.reporting import solar_energy_pv_electricity_battery
from xarsed.common.common import generate_list
from process.forms import UserLocationForm


def get_location(request):
    
    if request.method == "POST": 
        form = UserLocationForm(request.POST)

        if form.is_valid():
            form.save_location(request)
            
            selected_resource = "solarEnergyPV"
            series_parameters = series_parameter(selected_resource) 
            request.session["selected_resource"] = selected_resource

            request.session.set_expiry(3600)
            
            context = {"seriesParameters":series_parameters}

            return render(request, "process/get_resource.html", context)

    else:
        form = UserLocationForm()

    context = {
        "form": form,
    }

    return render(request, "process/get_location.html", context)


def resource_parameter(request, selectedParameter): 
        
    try:
        selected_resource = request.session["selected_resource"]
        series_parameters = series_parameter(selected_resource)  
        uploaded_file = request.FILES.get("uploadedFile")
        model = request.POST.get("model")

        if (uploaded_file == None and model == None):
                
            request.session.set_expiry(3600)
                
            message = "Please select at least one option!"
            context = {"message1": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
            return render(request, "process/get_resource.html", context)
            
        elif (uploaded_file != None and model != None):
                
            request.session.set_expiry(3600)
                
            message = "Please select at most one option!"
            context = {"message1": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
            return render(request, "process/get_resource.html", context)
            
        elif (uploaded_file != None and model == None):

            if uploaded_file.size > 2.5 * 1024 * 1024: #2.5MB

                request.session.set_expiry(3600)
                
                message = "Your file must be less than 2.5 MB in size!"
                context = {"message2": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                return render(request, "process/get_resource.html", context)
                
            else:

                if (uploaded_file.name.endswith(".csv") != True or uploaded_file.content_type != "text/csv"):

                    request.session.set_expiry(3600)
                
                    message = "Your file must be in CSV format!"
                    context = {"message2": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                    return render(request, "process/get_resource.html", context)
                    
                else:
                        
                    final_list = create_list(uploaded_file, selectedParameter)

                    if final_list == None:

                        request.session.set_expiry(3600)
                
                        message = "Please upload a file that contains only numbers and not all values ​​are zero!"
                        context = {"message2": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                        return render(request, "process/get_resource.html", context)
                        
                    else:

                        final_length = len(final_list)

                        if final_length != 8760: #number of hours per year
                                
                            request.session.set_expiry(3600)
                
                            message = "Your data should be 8760 steps, equivalent to the number of hours in a year!"
                            context = {"message2": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                            return render(request, "process/get_resource.html", context)
                            
                        else:

                            request.session[selectedParameter] = final_list
                            saved_parameters = []
                            for i in series_parameters:
                                try:
                                    request.session[i]
                                    saved_parameters.append(i)
                                except KeyError:
                                    continue

                            if set(series_parameters) != set(saved_parameters):
                                                                    
                                request.session.set_expiry(3600)
                
                                message = "Your data was saved successfully."
                                context = {"message4": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                                return render(request, "process/get_resource.html", context)
                                
                            else:
                                    
                                selected_requirement = "electricity"
                                series_parameters = series_parameter(selected_requirement) 
                                request.session["selected_requirement"] = selected_requirement

                                request.session.set_expiry(3600)
                
                                context = {"seriesParameters":series_parameters} 
                                
                                return render(request, "process/get_requirement.html", context)

        elif (uploaded_file == None and model != None):
  
            latitude = request.session["user_location"][1] 
            longitude = request.session["user_location"][0]
            time_difference = request.session["user_location"][2] 

            final_list = generate_list(selectedParameter, latitude, longitude, time_difference)

            if final_list == None:
                request.session.set_expiry(3600)

                message = "The requested parameter could not be saved, please try again!"
                context = {"message3": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                return render(request, "process/get_resource.html", context) 

            else:  
                request.session[selectedParameter] = final_list          
                
                saved_parameters = []
                for i in series_parameters:
                    try:
                        request.session[i]
                        saved_parameters.append(i)
                    except KeyError:
                        continue

                if set(series_parameters) != set(saved_parameters):
                                                                    
                    request.session.set_expiry(3600)
                            
                    message = "Your data was saved successfully."
                    context = {"message4": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                    return render(request, "process/get_resource.html", context)
                                
                else:
                                    
                    selected_requirement = "electricity"
                    series_parameters = series_parameter(selected_requirement) 
                    request.session["selected_requirement"] = selected_requirement

                    request.session.set_expiry(3600)
                
                    context = {"seriesParameters":series_parameters} 
                                
                    return render(request, "process/get_requirement.html", context) 

    except KeyError:
        return redirect("/home/")
      

def requirement_parameter(request, selectedParameter): 

    try:
        selected_requirement = request.session["selected_requirement"]
        series_parameters = series_parameter(selected_requirement)  
        uploaded_file = request.FILES.get("uploadedFile")

        if uploaded_file.size > 2.5 * 1024 * 1024: #2.5MB

            request.session.set_expiry(3600)
                
            message = "Your file must be less than 2.5 MB in size!"
            context = {"message1": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
            return render(request, "process/get_requirement.html", context)
                
        else:

            if (uploaded_file.name.endswith(".csv") != True or uploaded_file.content_type != "text/csv"):

                request.session.set_expiry(3600)
                
                message = "Your file must be in CSV format!"
                context = {"message1": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                return render(request, "process/get_requirement.html", context)
                    
            else:
                        
                final_list = create_list(uploaded_file, selectedParameter)

                if final_list == None:

                    request.session.set_expiry(3600)
                
                    message = "Please upload a file that contains only numbers and not all values ​​are zero!"
                    context = {"message1": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                    return render(request, "process/get_requirement.html", context)
                        
                else:

                    final_length = len(final_list)

                    if final_length != 8760: #number of hours per year
                                
                        request.session.set_expiry(3600)
                
                        message = "Your data should be 8760 steps, equivalent to the number of hours in a year!"
                        context = {"message1": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                        return render(request, "process/get_requirement.html", context)
                            
                    else:

                        request.session[selectedParameter] = final_list
                        saved_parameters = []
                        for i in series_parameters:
                            try:
                                request.session[i]
                                saved_parameters.append(i)
                            except KeyError:
                                continue

                        if set(series_parameters) != set(saved_parameters):
                                                                    
                            request.session.set_expiry(3600)
                
                            message = "Your data was saved successfully."
                            context = {"message2": message, "seriesParameters":series_parameters, "selectedParameter":selectedParameter} 
                            return render(request, "process/get_requirement.html", context)
                                
                        else:
                                    
                            request.session.set_expiry(3600)
                
                            return redirect("/process/final_report")
        
    except KeyError:

        return redirect("/home/")


def generate_data(request, selectedParameter): 
    
    try:
        request.session["selected_requirement"]

        consumption_table = request.session.get(selectedParameter+"_table", "")
        consumption_list = request.session.get(selectedParameter+"_list", [0 for i in range(8760)])
        
        request.session[selectedParameter+"_table"] = consumption_table
        request.session[selectedParameter+"_list"] = consumption_list

        applianceList, consumptionUnit = appliance_list(selectedParameter)

        request.session.set_expiry(3600)

        context = {"selectedParameter":selectedParameter, "applianceList":applianceList, "consumptionUnit":consumptionUnit, "consumptionTable":consumption_table}

        return render(request, "process/generate_data.html", context)
    
    except KeyError:

        return redirect("/home/")


def create_table(request, selectedParameter):

    try:
        consumption_table = request.session[selectedParameter+"_table"]
        consumption_list = request.session[selectedParameter+"_list"]
            
        appliance = request.POST.get("appliance")
        appliance_name = request.POST.get("applianceName")
        appliance_consumption = float(request.POST.get("applianceConsumption"))
        appliance_count = float(request.POST.get("applianceCount"))
        appliance_efficiency = float(request.POST.get("applianceEfficiency"))
        seasons = request.POST.getlist("season")
        months = request.POST.getlist("month")
        weeks = request.POST.getlist("week")
        days = request.POST.getlist("day")
        specfic_day = request.POST.get("specficDay")
        hours = request.POST.getlist("hour")
        appliance_usage = float(request.POST.get("applianceUsage"))

        new_consumption_table, new_consumption_list = generate_table_list(selectedParameter, appliance, appliance_name, appliance_consumption, appliance_count, appliance_efficiency, seasons, months, weeks, days, specfic_day, hours, appliance_usage, consumption_table, consumption_list)
            
        request.session[selectedParameter+"_table"] = new_consumption_table
        request.session[selectedParameter+"_list"] = new_consumption_list 
            
        applianceList, consumptionUnit = appliance_list(selectedParameter)

        request.session.set_expiry(3600)

        context = {"selectedParameter":selectedParameter, "applianceList":applianceList, "consumptionUnit":consumptionUnit, "consumptionTable":new_consumption_table}

        return render(request, "process/generate_data.html", context)
    
    except KeyError:

        return redirect("/home/")


def generate_csv(request, selectedParameter):

    try:
        import csv

        consumption_list = request.session[selectedParameter+"_list"]

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": "attachment; filename="+selectedParameter+".csv"},
        )

        writer = csv.writer(response)
    
        for i in consumption_list:
            writer.writerow([i])

        request.session.set_expiry(3600)

        return response
    
    except KeyError:

        return redirect("/home/")


def return_process(request, selectedParameter):

    try:
        request.session[selectedParameter+"_table"]
        request.session[selectedParameter+"_list"]
            
        selected_requirement = request.session["selected_requirement"] 
        series_parameters = series_parameter(selected_requirement) 

        request.session.set_expiry(3600)

        context = {"seriesParameters":series_parameters}

        return render(request, "process/get_requirement.html", context)
        
    except KeyError:

        return redirect("/home/")


def delete_table(request, selectedParameter):

    try:
        request.session[selectedParameter+"_table"]
        request.session[selectedParameter+"_list"]

        consumption_table = ""
        request.session[selectedParameter+"_table"] = consumption_table
        consumption_list = [0 for i in range(8760)]
        request.session[selectedParameter+"_list"] = consumption_list
            
        applianceList, consumptionUnit = appliance_list(selectedParameter)

        request.session.set_expiry(3600)

        context = {"selectedParameter":selectedParameter, "applianceList":applianceList, "consumptionUnit":consumptionUnit, "consumptionTable":consumption_table}

        return render(request, "process/generate_data.html", context)
    
    except KeyError:

        return redirect("/home/")


def final_report(request): 
  
    try:
        import os

        selected_resource = request.session["selected_resource"]
        selected_requirement = request.session["selected_requirement"]
        selected_storage = "battery"

        latitude = request.session["user_location"][1] 
        longitude = request.session["user_location"][0] 
        time_difference = request.session["user_location"][2]

        resource_series_parameters = series_parameter(selected_resource) 
        requirement_series_parameters = series_parameter(selected_requirement)

        resource_values = {}
        for i in resource_series_parameters:
            resource_values.update({i : request.session[i]})

        requirement_values = {}
        for i in requirement_series_parameters:
            requirement_values.update({i : request.session[i]})

        if (selected_resource == "solarEnergyPV" and selected_requirement == "electricity" and selected_storage == "battery"):
            solution_overview, solution_details = solar_energy_pv_electricity_battery(latitude, longitude, time_difference, resource_values, requirement_values)
                
        else:
            pass

        request.session["solution_overview"] = solution_overview
        request.session["solution_details"] = solution_details

        request.session.set_expiry(3600)  
            
        report_list = [solution_overview, solution_details]
        
        btc_address = os.environ.get("BTC_ADDRESS", "")
        
        context = {"reportList":report_list, "btcAddress": btc_address}

        return render(request, "process/final_report.html", context)
                  
    except KeyError:

        return redirect("/home/")
 
 
def save_html(request): 
  
    try: 
        report_list = [request.session["solution_overview"], request.session["solution_details"]]
            
        context = {"reportList":report_list}

        html_content = render_to_string("process/save_html.html", context)
            
        response = HttpResponse(html_content, content_type='text/html')
            
        response["Content-Disposition"] = "attachment; filename=Xarsed Final Report.html"
    
        return response
        
    except KeyError:

        return redirect("/home/")