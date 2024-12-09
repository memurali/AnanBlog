from django.urls import path
from . import views
from . import render
from . import get_ids
from base.views import commonViews


urlpatterns = [
    path('manage_services', render.Add_service),
    path('view_form', render.View_service),
    path('Service_index', render.Service_index),
    path('Service_details', render.Service_details),
    
    # Services 
    # Add Service 
    path('CategoryDetails', views.CategoryDetails, name='CategoryDetails'),
    path('getcategory', views.getcategory, name='getcategory'),
    path('findServiceDescription', views.findServiceDescription, name='findServiceDescription'),

    # Add Case Study 
    path('Add_CaseStudy', render.Add_CaseStudy, name='Add_CaseStudy'),
    path('view_CaseStudy', render.view_CaseStudy, name='view_CaseStudy'),
    path('CaseStudyDetails', views.CaseStudyDetails, name='CaseStudyDetails'),
    path('findServiceID', get_ids.findServiceID, name='findServiceID'),
    path('getCaseStudy', get_ids.getCaseStudy, name='getCaseStudy'),

    # Add Insights 
    path('Add_Insights', render.Add_Insights, name='Add_Insights'),
    path('view_Insights', render.view_Insights, name='view_Insights'),
    path('InsightsDetails', views.InsightsDetails, name='InsightsDetails'),
    path('getInsights', get_ids.getInsights, name='getInsights'),


    # Blogs 
    
    path('Blogs', render.blogs, name='blogs'),
    path('Blogs_details', render.blogs_details, name='blogs_details'),

    # ABout
    path('about', render.about, name='about'),
    path('contactus', render.contactus, name='contactus'),
    
    path('set_contact', commonViews.contact_us),
]