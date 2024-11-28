from django.urls import path
from . import views
from base.views import commonViews


urlpatterns = [
    path('manage_services', views.Add_service),
    path('view_form', views.View_service),
    path('Service_index', views.Service_index),
    path('Service_details', views.Service_details),
    
    path('CategoryDetails', views.CategoryDetails, name='CategoryDetails'),
    path('getcategory', views.getcategory, name='getcategory'),
    path('findServiceDescription', views.findServiceDescription, name='findServiceDescription'),

    # Blogs 
    
    path('Blogs', views.blogs, name='blogs'),
    path('Blogs_details', views.blogs_details, name='blogs_details'),

    # ABout
    path('about', views.about, name='about'),
    path('contactus', views.contactus, name='contactus'),
    
    path('set_contact', commonViews.contact_us),
]