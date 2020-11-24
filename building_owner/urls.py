from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
     path("building_owner", views.index, name="building_owner"),
     path("building_owner/home", views.index, name="building_owner"),
     path("building_owner/email/verification", views.v_email_verification, name="building_owner"),
     path("building_owner/email/verification/request", views.r_email_verification, name="building_owner")
]
