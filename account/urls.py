from django.urls import path;
from django.contrib import admin
from . import views, my_views

urlpatterns = [
     path("", my_views.login, name="account"),
     path("accounts", my_views.login, name="account"),
     path("accounts/login", my_views.login, name="account"),
     path("login/request", my_views.r_login_request, name="account"),
     path("logout", views.logout_request, name="account"),
     # path("register/building_owner", my_views.v_register_as_building_owner, name="account"),

     path("register/check/phone_number", my_views.r_check_phone_number_is_exists,
          name="account"),

     path("register", my_views.v_register, name="account"),
     path("register/building_owner/request", my_views.r_register_as_building_owner, name="account"),
     path("register/household/request", my_views.r_register_household, name="account"),

     path("register/check/username", my_views.r_check_username_exist, name="account"),
     path("register/purok", my_views.get_puroks_from_barangay, name="account")
]
