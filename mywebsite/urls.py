"""
Definition of urls for mywebsite.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from app import views


urlpatterns = [
    path('', views.home, name='home'),
   
]
