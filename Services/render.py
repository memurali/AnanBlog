from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Services 
@login_required
def Add_service(request):
    return render(request, 'services/Add_service.html')

@login_required
def View_service(request):
    return render(request, 'services/view_services.html')

@login_required
def Service_index(request):
    return render(request, 'services/Service_index.html')

@login_required
def Service_details(request):
    return render(request, 'services/Service_details.html')

# Case Study 
def Add_CaseStudy(request):
    return render(request, 'services/case_study.html')

def view_CaseStudy(request):
    return render(request, 'services/view_casestudy.html')

# Insights & Resources 

def Add_Insights(request):
    return render(request, 'services/insights.html')

def view_Insights(request):
    return render(request, 'services/view_insights.html')

# Blogs 
@login_required
def blogs(request):
    return render(request, 'Blogs/blog.html')


@login_required
def blogs_details(request):
    return render(request, 'Blogs/blog-detail.html')

# About 

def about(request):
    return render(request, 'about/about.html')

def contactus(request):
    return render(request, 'about/contactus.html')

def Login(request):
    return render(request, 'Blogs/login.html')

def Register(request):
    return render(request, 'Blogs/Signup.html')
