from django.urls import path
from django.views.generic import RedirectView
from . import views


app_name = "process"

urlpatterns = [
    path("get_location", views.get_location, name="get_location"),
    path("resource_parameter/<selectedParameter>/", views.resource_parameter, name="resource_parameter"),   
    path("requirement_parameter/<selectedParameter>/", views.requirement_parameter, name="requirement_parameter"), 
    path("generate_data/<selectedParameter>", views.generate_data, name="generate_data"), 
    path("create_table/<selectedParameter>", views.create_table, name="create_table"),
    path("generate_csv/<selectedParameter>", views.generate_csv, name="generate_csv"),
    path("return_process/<selectedParameter>/", views.return_process, name="return_process"),
    path("delete_table/<selectedParameter>", views.delete_table, name="delete_table"),
    path("final_report", views.final_report, name="final_report"),
    path("save_html", views.save_html, name="save_html"),
    path("", RedirectView.as_view(url="get_location")),
]