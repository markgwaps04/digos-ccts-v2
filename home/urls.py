from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
     path("home", views.index, name="account ")
]
