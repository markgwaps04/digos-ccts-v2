from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from modules import helpers
from django.contrib.auth.decorators import login_required, user_passes_test;
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib.auth.models import Group
# Create your views here.


# Create your views here.


class Category:

    that_building_owner = "Building Owner";
    that_citizens = "Citizens";


    map = {
        Group.objects.get(name=that_building_owner).id : "building_owner",
        Group.objects.get(name=that_citizens).id : "household"
    };

    group_building_owner_id = Group.objects.get(name=that_building_owner).id;
    group_citizens_id = Group.objects.get(name=that_citizens).id;


def should_not_staff_and_superuser(user):
    return not (user.is_superuser and user.is_staff);
    pass;

def should_building_owner(user):
    group_permission = user.groups.last();
    return Category.group_building_owner_id == group_permission.id;
    pass;

def should_household(user):
    group_permission = user.groups.last();
    return Category.group_citizens_id == group_permission.id;
    pass;

def should_superuser(user):
    return user.is_superuser;
    pass;

def logout_request(request):
    logout(request);
    return redirect("/");
    pass;

