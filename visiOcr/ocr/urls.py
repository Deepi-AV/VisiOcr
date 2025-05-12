from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home,name='home'),
    path('visitor-pass/', views.generate_pass, name='visitor_pass'),
]





