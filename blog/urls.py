from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogIndex),
    path('<str:catid>', views.blogIndexCat),
    path('details/<str:blogid>', views.articleDetails),
    path('blog/<int:blog_id>/download-pdf/', views.download_blog_pdf, name='download_blog_pdf')
]