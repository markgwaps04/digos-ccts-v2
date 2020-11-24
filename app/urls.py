"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include("account.urls")),
    path('', include("home.urls")),
    path('', include("building_owner.urls")),
    path('', include("household.urls")),
    path('', include("web_manage.urls")),
    path('', include("app_manage.urls")),
    path('', include("api.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);

admin.site.site_header = "Digos Covid Task Force Admin"
admin.site.site_title = "Covid Task Force Admin Portal"
admin.site.index_title = "Welcome to Covid Task Force Admin"
admin.site.site_url = "/home"
