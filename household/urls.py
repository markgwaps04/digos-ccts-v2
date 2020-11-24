from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
     path("household", views.index, name="household"),
     path("household/home", views.index, name="household"),
     path("household/phone_number/verification", views.v_phone_number_verification, name="household"),
     path("household/phone_number/verification/request", views.r_phone_number_verification, name="household"),
     path("household/family", views.family, name="household"),
     path("household/family/add/request", views.r_add_family_members, name="household"),
     path("household/family/add/cancel", views.cancel_request_adding_family_members, name="household"),
     path("household/family/qr_code", views.generate_id_card, name="household")
]
