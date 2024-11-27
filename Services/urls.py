from django.urls import path
from . import views

urlpatterns = [
    path('manage_services', views.Add_service),
    path('view_form', views.View_service),
    path('Service_index', views.Service_index),
    path('Service_details', views.Service_details),
    
    path('CategoryDetails', views.CategoryDetails, name='CategoryDetails'),
    path('getcategory', views.getcategory, name='getcategory'),
]