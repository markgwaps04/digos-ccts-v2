from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
     path("app", views.index, name="app"),
     path("app/login", views.login, name="app"),
     path("app/scan", views.scan, name="app")
]
