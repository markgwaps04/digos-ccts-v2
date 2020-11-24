from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test;
from account.views import Category, should_not_staff_and_superuser
import pdb;


# Create your views here.
@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser,login_url="/admin/home")
def index(request):

    group = request.user.groups.last();
    name = str(Category.map[group.id]).lower();

    return redirect("/" + name + "/home");

    pass;
