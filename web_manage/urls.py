from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
     path("admin/home", views.index, name="account"),
     path("admin/household", views.household_request, name="account"),
     path("admin/household/load/request", views.household_populate_request, name="account"),
     path("admin/household/members/state/request", views.changed_state_members_request, name="account"),
     path("admin/establishment", views.view_establishment_request, name="account"),
     path("admin/establishment/load/request", views.establishment_populate_request, name="account"),
     path("admin/establishment/state/request", views.establishment_state_change_request, name="account")
]
