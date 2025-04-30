from django.contrib.gis import forms


class UserLocationForm(forms.Form):
    
    user_location = forms.PointField(
        label = "Your Location",
        help_text = "Select your desired location on the map below. If you want to change your selected point, press the 'Delete All Features' button at the bottom of the map.", 
        widget = forms.OSMWidget(attrs={
            "template_name": "gis/openlayers-osm.html", 
            "default_lat": 0, 
            "default_lon": 0,
            "default_zoom": 0,
    }))
    
    def save_location(self, request):

        point_object = self.cleaned_data["user_location"]
        point_srid = point_object.srid
        point_coordinates = point_object.coords
        
        if point_srid == 4326:
            request.session["user_location"] = [point_coordinates[0], point_coordinates[1]]
        
        elif point_srid == 3857:
            transform_object = point_object.transform(4326, clone=True)

            if transform_object != None:
                transform_coordinates = transform_object.coords
                request.session["user_location"] = [transform_coordinates[0], transform_coordinates[1]]

            else:
                import math
                longitude = (point_coordinates[0] * 180) / 20037508.34
                lat = (point_coordinates[1] * 180) / 20037508.34
                latitude = (math.atan(math.pow(math.e, lat * (math.pi / 180))) * 360) / math.pi - 90
                request.session["user_location"] = [longitude, latitude]

