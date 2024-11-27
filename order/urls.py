from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderView),
    path('confirmation', views.ConfirmOrder),
    path('set', views.setOrder),
]