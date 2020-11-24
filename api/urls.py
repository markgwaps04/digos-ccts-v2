from django.urls import path;
from django.contrib import admin
from . import views

urlpatterns = [
     path("api", views.index, name="API Overview"),
     path("api/establishment/<str:username>", views.establishment_auth, name="task-establishment"),
]
