from django.urls import path
from . import views

urlpatterns = [
     
    path('', views.detect_page),
    path('analyze/', views.analyze),
     path('dashboard/', views.dashboard_page, name='dashboard') 
    
]
